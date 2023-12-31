@media print {
	/**
	 * MediaWiki print style sheet
	 * Largely based on work by Gabriel Wicke
	 *
	 * Originally derived from Plone (https://plone.org/) styles
	 * Copyright Alexander Limi
	 */
	
	/**
	 * Hide all the elements irrelevant for printing
	 */
	.noprint,
	#jump-to-nav,
	.mw-jump,
	#column-one,
	.mw-editsection,
	.mw-editsection-like,
	#footer-places,
	.mw-hidden-catlinks,
	.usermessage,
	.patrollink,
	.ns-0 .mw-redirectedfrom,
	.magnify,
	#mw-navigation,
	#siteNotice,
	/* Deprecated, changed in core */
	#f-poweredbyico,
	#f-copyrightico,
	li#about,
	li#disclaimer,
	li#mobileview,
	li#privacy {
		display: none;
	}
	
	/**
	 * Generic HTML elements
	 */
	body {
		background: #fff;
		color: #000;
		margin: 0;
		padding: 0;
	}
	
	h1,
	h2,
	h3,
	h4,
	h5,
	h6 {
		font-weight: bold;
		/* Pagination */
		page-break-after: avoid;
	}
	
	dt {
		font-weight: bold;
	}
	
	ul {
		list-style-type: square;
	}
	
	p {
		margin: 1em 0;
		line-height: 1.2em;
		/* Pagination */
		orphans: 3;
		widows: 3;
	}
	
	pre,
	.mw-code {
		background: #fff;
		color: #000;
		border: 1pt dashed #000;
		padding: 1em 0;
		font-size: 8pt;
		white-space: pre;
		word-wrap: break-word;
		overflow: auto;
	}
	
	img,
	figure,
	.wikitable,
	.thumb {
		/* Pagination */
		page-break-inside: avoid;
	}
	
	img {
		border: 0;
		vertical-align: middle;
	}
	
	/**
	 * MediaWiki-specific elements
	 */
	#globalWrapper {
		width: 100% !important;
		min-width: 0 !important;
	}
	
	.mw-body {
		background: #fff;
		color: #000;
		border: 0 !important;
		padding: 0 !important;
		margin: 0 !important;
		direction: ltr;
	}
	
	#column-content {
		margin: 0 !important;
	}
	
	#column-content .mw-body {
		padding: 1em;
		margin: 0 !important;
	}
	
	#toc {
		background-color: #f9f9f9;
		border: 1pt solid #aaa;
		padding: 5px;
		display: table;
	}
	
	/* Separate columns for tocnumber and toctext */
	.tocnumber,
	.toctext {
		display: table-cell;
	}
	
	/* Space between the columns for tocnumber and toctext */
	.tocnumber {
		padding-left: 0;
		padding-right: 0.5em;
	}
	
	/* @noflip */
	.mw-content-ltr .tocnumber {
		padding-left: 0;
		padding-right: 0.5em;
	}
	
	/* @noflip */
	.mw-content-rtl .tocnumber {
		padding-left: 0.5em;
		padding-right: 0;
	}
	
	#footer {
		background: #fff;
		color: #000;
		margin-top: 1em;
		border-top: 1pt solid #aaa;
		direction: ltr;
	}
	
	/**
	 * Links
	 */
	a {
		background: none !important;
		padding: 0 !important;
	}
	
	/* Expand URLs for printing */
	.mw-body a.external.text:after,
	.mw-body a.external.autonumber:after {
		content: " (" attr( href ) ")";
		word-break: break-all;
		word-wrap: break-word;
	}
	
	/* Expand protocol-relative URLs for printing */
	.mw-body a.external.text[href^='//']:after,
	.mw-body a.external.autonumber[href^='//']:after {
		content: " (https:" attr( href ) ")";
	}
	
	/* MSIE/Win doesn't understand 'inherit' */
	a,
	a.external,
	a.new,
	a.stub {
		color: #000 !important;
		text-decoration: none !important;
	}
	
	/* Continue ... */
	a,
	a.external,
	a.new,
	a.stub {
		color: inherit !important;
		text-decoration: inherit !important;
	}
	
	/**
	 * Floating divs
	 */
	/* @noflip */
	div.floatright {
		float: right;
		clear: right;
		position: relative;
		margin: 0.5em 0 0.8em 1.4em;
	}
	
	div.floatright p {
		font-style: italic;
	}
	
	/* @noflip */
	div.floatleft {
		float: left;
		clear: left;
		position: relative;
		margin: 0.5em 1.4em 0.8em 0;
	}
	
	div.floatleft p {
		font-style: italic;
	}
	
	.center {
		text-align: center;
	}
	
	/**
	 * Thumbnails
	 */
	div.thumb {
		background-color: transparent;
		border: 0;
		width: auto;
		margin-top: 0.5em;
		margin-bottom: 0.8em;
	}
	
	div.thumbinner {
		background-color: #fff;
		border: 1pt solid #ccc;
		padding: 3px;
		font-size: 94%;
		text-align: center;
		/* new block formatting context,
		 * to clear background from floating content  */
		overflow: hidden;
	}
	
	html .thumbimage {
		border: 1pt solid #ccc;
	}
	
	html .thumbcaption {
		border: none;
		text-align: left;
		line-height: 1.4em;
		padding: 3px;
		font-size: 94%;
	}
	
	/* @noflip */
	div.tright {
		float: right;
		clear: right;
		margin: 0.5em 0 0.8em 1.4em;
	}
	
	/* @noflip */
	div.tleft {
		float: left;
		clear: left;
		margin: 0.5em 1.4em 0.8em 0;
	}
	
	img.thumbborder {
		border: 1pt solid #ddd;
	}
	
	/**
	 * Table rendering
	 * As on shared.css but with white background.
	 */
	table.wikitable,
	table.mw_metadata {
		background: #fff;
		margin: 1em 0;
		border: 1pt solid #aaa;
		border-collapse: collapse;
	}
	
	table.wikitable > tr > th,
	table.wikitable > tr > td,
	table.wikitable > * > tr > th,
	table.wikitable > * > tr > td,
	.mw_metadata th,
	.mw_metadata td {
		border: 1pt solid #aaa;
		padding: 0.2em;
	}
	
	table.wikitable > tr > th,
	table.wikitable > * > tr > th,
	.mw_metadata th {
		background: #fff;
		font-weight: bold;
		text-align: center;
	}
	
	table.wikitable > caption,
	.mw_metadata caption {
		font-weight: bold;
	}
	
	table.listing,
	table.listing td {
		border: 1pt solid #000;
		border-collapse: collapse;
	}
	
	/**
	 * Categories
	 */
	.catlinks ul {
		display: inline;
		padding: 0;
		list-style: none none;
	}
	
	.catlinks li {
		display: inline-block;
		line-height: 1.15em;
		padding: 0 .4em;
		border-left: 1pt solid #aaa;
		margin: 0.1em 0;
	}
	
	.catlinks li:first-child {
		padding-left: .2em;
		border-left: 0;
	}
	
	.printfooter {
		padding: 1em 0;
	}}