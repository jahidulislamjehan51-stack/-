<?php
header('Content-Type: application/json');

// ছবি সেভ করার ফোল্ডার
$storage = "photo/";
if (!is_dir($storage)) {
    mkdir($storage, 0777, true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['pdf'])) {
    $pdf = $_FILES['pdf']['tmp_name'];
    
    // ১. টেক্সট এবং ডাটা কালেকশন (অটোমেটেড)
    $text = shell_exec("pdftotext -layout " . escapeshellarg($pdf) . " -");

    function findData($start, $end, $content) {
        $pattern = '/' . preg_quote($start) . '(.*?)' . preg_quote($end) . '/s';
        if (preg_match($pattern, $content, $m)) return trim(str_replace('"', '', $m[1]));
        return "";
    }

    // আপনার পিডিএফ এর নির্দিষ্ট ঘর থেকে তথ্য সংগ্রহ
    $nid    = findData('National ID', 'Pin', $text);
    $pin    = findData('Pin', 'Status', $text);
    $names  = findData('Name(English)', 'Date of Birth', $text);
    $nameArray = explode("\n", trim($names));
    
    $father = findData('Father Name', 'Mother Name', $text);
    $mother = findData('Mother Name', 'Spouse Name', $text);
    $dob    = findData('Date of Birth', 'Birth Place', $text);
    $blood  = findData('Blood Group', '--- PAGE', $text); // ২য় পাতা থেকে
    
    // ঠিকানা অটোমেশন (Present Address থেকে সংগ্রহ)
    $addressRaw = findData('Present Address', 'Permanent Address', $text);
    $cleanAddress = str_replace(["\n", "  "], " ", $addressRaw);

    // ২. ছবি ও স্বাক্ষর কালেকশন (অটোমেটেড ক্রপ)
    // এটি পিডিএফ থেকে সব ছবি বের করবে
    shell_exec("pdfimages -j " . escapeshellarg($pdf) . " " . $storage . "img");

    // সাধারণত ভোটার ফরমের প্রথম ছবিটি স্বাক্ষর এবং দ্বিতীয়টি মূল ফটো হয়
    $finalPhoto = $storage . "img-001.jpg"; 
    $finalSign  = $storage . "img-000.jpg";

    // ৩. ফাইনাল আউটপুট (যা আপনার nid.php তে সরাসরি বসে যাবে)
    echo json_encode([
        "status" => "success",
        "data" => [
            "nid"           => trim($nid, " ,"),
            "pin"           => trim($pin, " ,"),
            "nameBangla"    => trim($nameArray[0] ?? ""),
            "nameEnglish"   => trim($nameArray[1] ?? ""),
            "fatherName"    => trim($father, " ,"),
            "motherName"    => trim($mother, " ,"),
            "dateOfBirth"   => trim($dob, " ,"),
            "bloodGroup"    => trim($blood, " ,"),
            "address"       => trim($cleanAddress)
        ],
        "images" => [
            "photo" => file_exists($finalPhoto) ? $finalPhoto : "assets/media/card/blank.png",
            "signature" => file_exists($finalSign) ? $finalSign : "assets/media/card/blank.png"
        ]
    ]);
    exit;
}
