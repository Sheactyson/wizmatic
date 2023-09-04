@media screen {
	/**
	 * MediaWiki style sheet for general styles on basic content elements
	 *
	 * Styles for basic elements: links, lists, etc...
	 *
	 * This style sheet is used by the Monobook and Vector skins.
	 */
	
	/* Links */
	a {
		text-decoration: none;
		color: #0645ad;
		background: none;
	}
	
	a:not( [href] ) {
		cursor: pointer; /* Always cursor:pointer even without href */
	}
	
	a:visited {
		color: #0b0080;
	}
	
	a:active {
		color: #faa700;
	}
	
	a:hover, a:focus {
		text-decoration: underline;
	}
	
	a:lang(ar),
	a:lang(kk-arab),
	a:lang(mzn),
	a:lang(ps),
	a:lang(ur) {
		text-decoration: none;
	}
	
	a.stub {
		color: #723;
	}
	
	a.new, #p-personal a.new {
		color: #ba0000;
	}
	
	a.new:visited, #p-personal a.new:visited {
		color: #a55858;
	}
	
	/* Interwiki Styling */
	.mw-body a.extiw,
	.mw-body a.extiw:active {
		color: #36b;
	}
	
	.mw-body a.extiw:visited {
		color: #636;
	}
	
	.mw-body a.extiw:active {
		color: #b63;
	}
	
	/* External links */
	.mw-body a.external {
		color: #36b;
	}
	
	.mw-body a.external:visited {
		color: #636; /* bug 3112 */
	}
	
	.mw-body a.external:active {
		color: #b63;
	}
	
	.mw-body a.external.free {
		word-wrap: break-word;
	}
	
	/* Inline Elements */
	img {
		border: none;
		vertical-align: middle;
	}
	
	hr {
		height: 1px;
		color: #aaa;
		background-color: #aaa;
		border: 0;
		margin: .2em 0;
	}
	
	/* Structural Elements */
	h1,
	h2,
	h3,
	h4,
	h5,
	h6 {
		color: #000;
		background: none;
		font-weight: normal;
		margin: 0;
		overflow: hidden;
		padding-top: .5em;
		padding-bottom: .17em;
		border-bottom: 1px solid #aaa;
	}
	
	h1 {
		font-size: 188%;
	}
	
	h2 {
		font-size: 150%;
	}
	
	h3,
	h4,
	h5,
	h6 {
		border-bottom: none;
		font-weight: bold;
	}
	
	h3 {
		font-size: 128%;
	}
	
	h4 {
		font-size: 116%;
	}
	
	h5 {
		font-size: 108%;
	}
	
	h6 {
		font-size: 100%;
	}
	
	/* Some space under the headers in the content area */
	h1,
	h2 {
		margin-bottom: .6em;
	}
	
	h3,
	h4,
	h5 {
		margin-bottom: .3em;
	}
	
	p {
		margin: .4em 0 .5em 0;
	}
	
	p img {
		margin: 0;
	}
	
	ul {
		list-style-type: square;
		margin: .3em 0 0 1.6em;
		padding: 0;
	}
	
	ol {
		margin: .3em 0 0 3.2em;
		padding: 0;
		list-style-image: none;
	}
	
	li {
		margin-bottom: .1em;
	}
	
	dt {
		font-weight: bold;
		margin-bottom: .1em;
	}
	
	dl {
		margin-top: .2em;
		margin-bottom: .5em;
	}
	
	dd {
		margin-left: 1.6em;
		margin-bottom: .1em;
	}
	
	pre, code, tt, kbd, samp, .mw-code {
		/*
		 * Some browsers will render the monospace text too small, namely Firefox, Chrome and Safari.
		 * Specifying any valid, second value will trigger correct behavior without forcing a different font.
		 */
		font-family: monospace, 'Courier';
	}
	
	code {
		color: #000;
		background-color: #f9f9f9;
		border: 1px solid #ddd;
		border-radius: 2px;
		padding: 1px 4px;
	}
	
	pre,
	.mw-code {
		color: #000;
		background-color: #f9f9f9;
		border: 1px solid #ddd;
		padding: 1em;
		/* Wrap lines in overflow. T2260, T103780 */
		white-space: pre-wrap;
	}
	
	/* Tables */
	table {
		font-size: 100%;
	}
	
	/* Forms */
	fieldset {
		border: 1px solid #2f6fab;
		margin: 1em 0 1em 0;
		padding: 0 1em 1em;
	}
	
	fieldset.nested {
		margin: 0 0 0.5em 0;
		padding: 0 0.5em 0.5em;
	}
	
	legend {
		padding: .5em;
		font-size: 95%;
	}
	
	form {
		border: none;
		margin: 0;
	}
	
	textarea {
		width: 100%;
		padding: .1em;
		display: block;
		-moz-box-sizing: border-box;
		-webkit-box-sizing: border-box;
		box-sizing: border-box;
	}
	
	/* Emulate Center */
	.center {
		width: 100%;
		text-align: center;
	}
	
	*.center * {
		margin-left: auto;
		margin-right: auto;
	}
	
	/* Small for tables and similar */
	.small {
		font-size: 94%;
	}
	
	table.small {
		font-size: 100%;
	}
	
	/**
	 * MediaWiki style sheet for general styles on complex content
	 *
	 * Styles for complex things which are a standard part of page content
	 * (ie: the CSS classing built into the system), like the TOC.
	 */
	
	/* Table of Contents */
	#toc,
	.toc,
	.mw-warning,
	.toccolours {
		border: 1px solid #aaa;
		background-color: #f9f9f9;
		padding: 5px;
		font-size: 95%;
	}
	
	/**
	 * We want to display the ToC element with intrinsic width in block mode. The fit-content
	 * value for width is however not supported by large groups of browsers.
	 *
	 * We use display:table. Even though it should only contain other table-* display
	 * elements, there are no known problems with using this.
	 *
	 * Because IE < 8 and other older browsers don't support display:table, we fallback to
	 * using inline-block mode, which features at least intrinsic width, but won't clear preceding
	 * inline elements. In practice inline elements surrounding the TOC are uncommon enough that
	 * this is an acceptable sacrifice.
	 */
	#toc,
	.toc {
		display: inline-block;
		display: table;
	
		/* IE7 and earlier */
		zoom: 1;
		*display: inline;
	
		padding: 7px;
	}
	
	/* CSS for backwards-compatibility with cached page renders and creative uses in wikitext */
	table#toc,
	table.toc {
		border-collapse: collapse;
	}
	
	/* Remove additional paddings inside table-cells that are not present in <div>s */
	table#toc td,
	table.toc td {
		padding: 0;
	}
	
	#toc h2,
	.toc h2 {
		display: inline;
		border: none;
		padding: 0;
		font-size: 100%;
		font-weight: bold;
	}
	
	#toc #toctitle,
	.toc #toctitle,
	#toc .toctitle,
	.toc .toctitle {
		text-align: center;
	}
	
	#toc ul,
	.toc ul {
		list-style-type: none;
		list-style-image: none;
		margin-left: 0;
		padding: 0;
		text-align: left;
	}
	
	#toc ul ul,
	.toc ul ul {
		margin: 0 0 0 2em;
	}
	
	/* Separate columns for tocnumber and toctext */
	/* Ignored by IE7 and lower */
	.tocnumber,
	.toctext {
		display: table-cell;
		/*
		Text decorations are not propagated to the contents of inline blocks and inline tables,
		according to <http://www.w3.org/TR/css-text-decor-3/#line-decoration>, and 'display: table-cell'
		generates an inline table when used without any parent table-rows and tables.
		*/
		text-decoration: inherit;
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
	
	/* Warning */
	.mw-warning {
		margin-left: 50px;
		margin-right: 50px;
		text-align: center;
	}
	
	/* Images */
	/* @noflip */div.floatright, table.floatright {
		margin: 0 0 .5em .5em;
		border: 0;
	}
	
	div.floatright p {
		font-style: italic;
	}
	
	/* @noflip */div.floatleft, table.floatleft {
		margin: 0 .5em .5em 0;
		border: 0;
	}
	
	div.floatleft p {
		font-style: italic;
	}
	
	/* Thumbnails */
	div.thumb {
		margin-bottom: .5em;
		width: auto;
		background-color: transparent;
	}
	
	div.thumbinner {
		border: 1px solid #ccc;
		padding: 3px;
		background-color: #f9f9f9;
		font-size: 94%;
		text-align: center;
		/* new block formatting context,
		 * to clear background from floating content  */
		overflow: hidden;
	}
	
	html .thumbimage {
		border: 1px solid #ccc;
	}
	
	html .thumbcaption {
		border: none;
		line-height: 1.4em;
		padding: 3px;
		font-size: 94%;
		/* Default styles when there's no .mw-content-ltr or .mw-content-rtl, overridden below */
		text-align: left;
	}
	
	div.magnify {
		/* Default styles when there's no .mw-content-ltr or .mw-content-rtl, overridden below */
		float: right;
		margin-left: 3px;
	}
	
	div.magnify a {
		display: block;
		/* Hide the text… */
		text-indent: 15px;
		white-space: nowrap;
		overflow: hidden;
		/* …and replace it with the image */
		width: 15px;
		height: 11px;
		/* Default styles when there's no .mw-content-ltr or .mw-content-rtl, overridden below */
	
		/* Use same SVG support hack as mediawiki.legacy's shared.css */
		background-image: url(/wiki/resources/src/mediawiki.skinning/images/magnify-clip-ltr.png?4f704);
		background-image: linear-gradient( transparent, transparent ), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%20standalone%3D%22no%22%3F%3E%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2011%2015%22%20width%3D%2215%22%20height%3D%2211%22%3E%0A%20%20%20%20%3Cg%20id%3D%22magnify-clip%22%20fill%3D%22%23fff%22%20stroke%3D%22%23000%22%3E%0A%20%20%20%20%20%20%20%20%3Cpath%20id%3D%22bigbox%22%20d%3D%22M1.509%201.865h10.99v7.919h-10.99z%22%2F%3E%0A%20%20%20%20%20%20%20%20%3Cpath%20id%3D%22smallbox%22%20d%3D%22M-1.499%206.868h5.943v4.904h-5.943z%22%2F%3E%0A%20%20%20%20%3C%2Fg%3E%0A%3C%2Fsvg%3E%0A);
		background-image: linear-gradient( transparent, transparent ), url(/wiki/resources/src/mediawiki.skinning/images/magnify-clip-ltr.svg?7fa0a)!ie;
		/* Don't annoy people who copy-paste everything too much */
		-moz-user-select: none;
		-webkit-user-select: none;
		-ms-user-select: none;
		user-select: none;
	}
	
	img.thumbborder {
		border: 1px solid #ddd;
	}
	
	/* Directionality-specific styles for thumbnails - their positioning depends on content language */
	
	/* @noflip */
	.mw-content-ltr .thumbcaption {
		text-align: left;
	}
	
	/* @noflip */
	.mw-content-ltr .magnify {
		float: right;
		margin-left: 3px;
		margin-right: 0;
	}
	
	/* @noflip */
	.mw-content-ltr div.magnify a {
		/* Use same SVG support hack as mediawiki.legacy's shared.css */
		background-image: url(/wiki/resources/src/mediawiki.skinning/images/magnify-clip-ltr.png?4f704);
		background-image: linear-gradient( transparent, transparent ), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%20standalone%3D%22no%22%3F%3E%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2011%2015%22%20width%3D%2215%22%20height%3D%2211%22%3E%0A%20%20%20%20%3Cg%20id%3D%22magnify-clip%22%20fill%3D%22%23fff%22%20stroke%3D%22%23000%22%3E%0A%20%20%20%20%20%20%20%20%3Cpath%20id%3D%22bigbox%22%20d%3D%22M1.509%201.865h10.99v7.919h-10.99z%22%2F%3E%0A%20%20%20%20%20%20%20%20%3Cpath%20id%3D%22smallbox%22%20d%3D%22M-1.499%206.868h5.943v4.904h-5.943z%22%2F%3E%0A%20%20%20%20%3C%2Fg%3E%0A%3C%2Fsvg%3E%0A);
		background-image: linear-gradient( transparent, transparent ), url(/wiki/resources/src/mediawiki.skinning/images/magnify-clip-ltr.svg?7fa0a)!ie;
	}
	
	/* @noflip */
	.mw-content-rtl .thumbcaption {
		text-align: right;
	}
	
	/* @noflip */
	.mw-content-rtl .magnify {
		float: left;
		margin-left: 0;
		margin-right: 3px;
	}
	
	/* @noflip */
	.mw-content-rtl div.magnify a {
		/* Use same SVG support hack as mediawiki.legacy's shared.css */
		background-image: url(/wiki/resources/src/mediawiki.skinning/images/magnify-clip-rtl.png?a9fb3);
		background-image: linear-gradient( transparent, transparent ), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%20standalone%3D%22no%22%3F%3E%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2011%2015%22%20width%3D%2215%22%20height%3D%2211%22%3E%0A%20%20%20%20%3Cg%20id%3D%22magnify-clip%22%20fill%3D%22%23fff%22%20stroke%3D%22%23000%22%3E%0A%20%20%20%20%20%20%20%20%3Cpath%20id%3D%22bigbox%22%20d%3D%22M9.491%201.865h-10.99v7.919h10.99z%22%2F%3E%0A%20%20%20%20%20%20%20%20%3Cpath%20id%3D%22smallbox%22%20d%3D%22M12.499%206.868h-5.943v4.904h5.943z%22%2F%3E%0A%20%20%20%20%3C%2Fg%3E%0A%3C%2Fsvg%3E%0A);
		background-image: linear-gradient( transparent, transparent ), url(/wiki/resources/src/mediawiki.skinning/images/magnify-clip-rtl.svg?96de0)!ie;
	}
	
	/* @noflip */
	div.tright {
		margin: .5em 0 1.3em 1.4em;
	}
	
	/* @noflip */
	div.tleft {
		margin: .5em 1.4em 1.3em 0;
	}
	
	/* Hide elements that are marked as "empty" according to legacy Tidy rules,
	 * except if a client script removes the mw-hide-empty-elt class from the body
	 */
	body.mw-hide-empty-elt .mw-empty-elt {
		display: none;
	}
	
	/**
	 * MediaWiki style sheet for common core styles on interfaces
	 *
	 * Styles for the Monobook/Vector pattern of laying out common interfaces.
	 * These ids/classes are not built into the system,
	 * they are outputted by the actual MonoBook/Vector code by convention.
	 */
	
	/* Categories */
	.catlinks {
		border: 1px solid #aaa;
		background-color: #f9f9f9;
		padding: 5px;
		margin-top: 1em;
		clear: both;
	}
	
	textarea {
		/* Support Firefox: Border rule required to override system appearance on Linux */
		border: 1px solid #c0c0c0;
	}
	
	.editOptions {
		background-color: #f0f0f0;
		border: 1px solid #c0c0c0;
		border-top: none;
		padding: 1em 1em 1.5em 1em;
		margin-bottom: 2em;
	}
	
	.usermessage {
		background-color: #ffce7b;
		border: 1px solid #ffa500;
		color: #000;
		font-weight: bold;
		margin: 2em 0 1em;
		padding: .5em 1em;
		vertical-align: middle;
	}
	
	#siteNotice {
		position: relative;
		text-align: center;
		margin: 0;
	}
	
	#localNotice {
		margin-bottom: 0.9em;
	}
	
	.firstHeading {
		margin-bottom: .1em;
		/* These two rules hack around bug 2013 (fix for more limited bug 11325).
		 * When bug 2013 is fixed properly, they should be removed. */
		line-height: 1.2em;
		padding-bottom: 0;
	}
	
	/* Sub-navigation */
	#siteSub {
		display: none;
	}
	
	#jump-to-nav {
		/* Negate #contentSub's margin and replicate it so that the jump to links don't affect the spacing */
		margin-top: -1.4em;
		margin-bottom: 1.4em;
	}
	
	#contentSub,
	#contentSub2 {
		font-size: 84%;
		line-height: 1.2em;
		margin: 0 0 1.4em 1em;
		color: #545454;
		width: auto;
	}
	
	span.subpages {
		display: block;
	}}.mw-wiki-logo { background-image: url(/wiki/skins/common/images/w101c-wiki.png?79609); }