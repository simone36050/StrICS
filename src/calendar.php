<?php

function error() {
    http_response_code(400);
    die;
}

// get filters
$filters = array();

if(isset($_GET['filters'])) {
    $filt = $_GET['filters'];

    if(!is_array($filt)) 
        error();

    // check and parse input
    foreach($filt as $elm) {
        $split = explode("|", $elm);
        if(count($split) !== 2)
            error();

        $filters[] = array("sector" => strtolower($split[0]), "region" => strtolower($split[1]));
    }
}

// execute python script
$input = json_encode($filters);
$output = array();
exec("python3 calculator.py " . escapeshellarg($input) . " 2>&1", $output);

header('Content-type: text/plain; charset=utf-8');

echo implode("\n", $output);
