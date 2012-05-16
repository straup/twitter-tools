<?php

	define(ROOT, dirname(__FILE__) . "/");
	define(FPDF, ROOT . "lib/php/fpdf16/");
	define(QR, ROOT . "lib/php/qr/");
	define(FLAMEWORK, ROOT . "lib/php/flamework/");

	require_once(FPDF . "fpdf.php");
	require_once(QR. "qr.php");
	require_once(FLAMEWORK . "lib_cli.php");

	# FIX ME: is this even necessary?
	date_default_timezone_set('America/Los_Angeles');

	# This assumes individual tweets written as JSON files
	# and stored in YMD style directories. See also:
	# backup_tweets.py

	# TO DO: date ranges not just single years
	# TO DO: keep track of all the tmp files and ensure
	# they are deleted at the end of the program

	#########################################################

	# main() is located at the bottom of the page

	#######################################################

	class twPDF extends FPDF {

		function twPDF($year, $user){

			$this->FPDF("P", "in", array(6, 9));

			$this->year = $year;
			$this->username = $user;

			$this->tweet = null;
			$this->text_align = null;
		}

		function setup_margins(){

			if ($this->PageNo() % 2){
				$this->SetMargins(1.25, 1.5);
				$this->text_align = 'L';
			}

			else {
				$this->SetMargins(1, 1.5);
				$this->SetRightMargin(1.25);
				$this->text_align = 'R';
			}
		}

		function draw($src, $outfile){

			$files = array();
			$this->walk_dir($src, $files);

			$this->AddPage();
			$this->AddPage();

			$year = basename($src);
			$title = "#{$this->year}";

			$this->AddPage();
			$this->SetRightMargin(1.25);
			$this->SetFont('Helvetica','B', 51);
			$this->SetTextColor(126, 126, 126);
			$this->setY(-2.25);
			$this->MultiCell(0, 1, $title, 0, 'R');

			$this->SetFont('Helvetica','B', 18);
			$this->MultiCell(0, 0, $this->username, 0, 'R');

			$this->AddPage();

			$pages = array();
			$index = array();

			foreach ($files as $path){

				$this->tweet = $this->parse($path);

				if (! $this->tweet){
					continue;
				}

				if ($this->tweet['epilogue']){

					if ($this->PageNo() % 2){
						$this->addPage();
					}

					$this->addPage();
					$this->addPage();

					$this->addPage();
					$this->SetTextColor(0);
					$this->SetMargins(1, 1);
					$this->SetY(-2);
					$this->SetX(3);
					$this->SetFont('Helvetica', 'B', 24);
					$this->MultiCell(2, .2, "#epilogue", 0, 'L');

					$this->AddPage();
				}

				$this->setup_margins();
				$this->AddPage();

				$this->SetFont('Helvetica','B', 24);
				$this->SetTextColor(0);
				$this->MultiCell(0, .5, $this->tweet['text'], 0, $this->text_align);

				$qr_img = $this->generate_qrcode($this->tweet['url']);

				$qr_pos = -2.25;
				$dt_pos = -1.25;

				$this->setY($qr_pos);

				if ($this->text_align == 'R'){
					$this->setX(-2.20);
				}

				else {
					$this->setX(1.2);
				}

				$this->Image($qr_img, null, null, 1, 1);
				unlink($qr_img);

				$this->SetY($dt_pos);

				$this->SetFont('Helvetica','B', 10);
				$this->SetTextColor(126, 126, 126);
				$this->MultiCell(0, .25, $this->tweet['date'], 0, $this->text_align);

				if ($this->tweet['epilogue']){
					break;
				}
			}

			$this->draw_colophon($this->username);

			$this->Output($outfile);
		}

		function generate_qrcode($text){

			$qr_args = array(
				'data' => QR . "data",
				'images' => QR . "image"
			);

			$enc = md5($text);
			$qr_img_black = tempnam("/tmp", time()) . "qr-{$enc}.png";

			$qr = new QR($qr_args);

			$args = array(
				'd' => $text,
				'path' => $qr_img_black,
			);

			$qr->encode($args);

			$im_black = imagecreatefrompng($qr_img_black);
			imagecolorset($im_black, 1, 126, 126, 126);
			imagepng($im_black, $qr_img_black);

			return $qr_img_black;
		}

		function draw_colophon($name=''){

			if ($full_name == ''){
				return;
			}

			if ($this->PageNo() % 2){
				$this->addPage();
			}

			$this->addPage();
			$this->addPage();

			$this->addPage();
			$this->SetTextColor(0);
			$this->SetMargins(1, 1);
			$this->SetY(-2);
			$this->SetX(3);
			$this->SetFont('Helvetica', 'B', 12);
			$this->MultiCell(2, .2, "this is a thing made by {$name}", 0, 'R');
		}

		function walk_dir($root, &$files){

			foreach (scandir($root) as $path){

				if (preg_match("/^\.+$/", $path)){
					continue;
				}

				$path = "{$root}/{$path}";

				if (is_file($path)){
					$files[] = $path;
					continue;
				}

				if (is_dir($path)){
					$this->walk_dir($path, $files);
				}
			}
		}

		function load_tweet($path){

			$fh = fopen($path, 'r');
			$json = fread($fh, filesize($path));
			fclose($fh);

			return json_decode($json, "as hash");
		}

		function parse($path){

			$data = $this->load_tweet($path);
			$date = strtotime($data['created_at']);

			$year = date("Y", $date);
			$ymd = date("F d, Y", $date);

			if ($year < $this->year){
				return null;
			}

			$text = html_entity_decode($data['text']);
			$text = iconv("UTF-8", "ISO-8859-1//TRANSLIT", $text);

			$id = $data['id'];

			$rsp = array(
				'id' => $id,
				'url' => "http://twitter.com/{$this->username}/status/{$id}",
				'date' => $ymd,
				'text' => $text,
			);

			if ($year > $this->year){
				$rsp['epilogue'] = 1;
			}

			return $rsp;
		}

	}

	#########################################################

	# main()

	$spec = array(
		"tweets" => array("flag" => "t", "required" => 1, "help" => "The path to your archived Tweets, as generated by the backup_tweets.py script."),
		"output" => array("flag" => "o", "required" => 1, "help" => "The path for the final PDF file you're creating."),
		"username" => array("flag" => "u", "required" => 0, "help" => "The username of the person whose Tweets you're creating a book of. Unfortunately this information is not store in individual Tweets so you need to define it explicitly if you want it to appear in the book."),
		"year" => array("flag" => "y", "required" => 0, "help" => "The year of Tweets you're created a book of. Defaults to the current year."),
	);

	$opts = cli_getopts($spec);

	$src = $opts['tweets'];
	$out = $opts['output'];

	$year = (isset($opts['year'])) ? $opts['year'] : date('Y', time());
	$user = $opts['username'];

	$tw = new twPDF($year, $user);
	$tw->draw($src, $out);

	echo "- done -\n";
	exit;

	#########################################################

?>
