/*
 * qTip2 - Pretty powerful tooltips - v2.2.1
 * http://qtip2.com
 *
 * Copyright (c) 2014 
 * Released under the MIT licenses
 * http://jquery.org/license
 *
 * Date: Sun Sep 7 2014 12:01 EDT-0400
 * Plugins: tips viewport
 * Styles: core css3
 */
.qtip{
	position: absolute;
	left: -28000px;
	top: -28000px;
	display: none;

	max-width: 280px;
	min-width: 50px;

	font-size: 10.5px;
	line-height: 12px;

	direction: ltr;

	box-shadow: none;
	padding: 0;
}

	.qtip-content{
		position: relative;
		padding: 5px 9px;
		overflow: hidden;

		text-align: left;
		word-wrap: break-word;
	}

	.qtip-titlebar{
		position: relative;
		padding: 5px 35px 5px 10px;
		overflow: hidden;

		border-width: 0 0 1px;
		font-weight: bold;
	}

	.qtip-titlebar + .qtip-content{ border-top-width: 0 !important; }

	/* Default close button class */
	.qtip-close{
		position: absolute;
		right: -9px; top: -9px;
		z-index: 11; /* Overlap .qtip-tip */

		cursor: pointer;
		outline: medium none;

		border: 1px solid transparent;
	}

		.qtip-titlebar .qtip-close{
			right: 4px; top: 50%;
			margin-top: -9px;
		}

		* html .qtip-titlebar .qtip-close{ top: 16px; } /* IE fix */

		.qtip-titlebar .ui-icon,
		.qtip-icon .ui-icon{
			display: block;
			text-indent: -1000em;
			direction: ltr;
		}

		.qtip-icon, .qtip-icon .ui-icon{
			-moz-border-radius: 3px;
			-webkit-border-radius: 3px;
			border-radius: 3px;
			text-decoration: none;
		}

			.qtip-icon .ui-icon{
				width: 18px;
				height: 14px;

				line-height: 14px;
				text-align: center;
				text-indent: 0;
				font: normal bold 10px/13px Tahoma,sans-serif;

				color: inherit;
				background: transparent none no-repeat -100em -100em;
			}

/* Applied to 'focused' tooltips e.g. most recently displayed/interacted with */
.qtip-focus{}

/* Applied on hover of tooltips i.e. added/removed on mouseenter/mouseleave respectively */
.qtip-hover{}

/* Default tooltip style */
.qtip-default{
	border: 1px solid #F1D031;

	background-color: #FFFFA3;
	color: #555;
}

	.qtip-default .qtip-titlebar{
		background-color: #FFEF93;
	}

	.qtip-default .qtip-icon{
		border-color: #CCC;
		background: #F1F1F1;
		color: #777;
	}

	.qtip-default .qtip-titlebar .qtip-close{
		border-color: #AAA;
		color: #111;
	}


.qtip-shadow{
	-webkit-box-shadow: 1px 1px 3px 1px rgba(0, 0, 0, 0.15);
	-moz-box-shadow: 1px 1px 3px 1px rgba(0, 0, 0, 0.15);
	box-shadow: 1px 1px 3px 1px rgba(0, 0, 0, 0.15);
}

/* Add rounded corners to your tooltips in: FF3+, Chrome 2+, Opera 10.6+, IE9+, Safari 2+ */
.qtip-rounded,
.qtip-tipsy,
.qtip-bootstrap{
	-moz-border-radius: 5px;
	-webkit-border-radius: 5px;
	border-radius: 5px;
}

.qtip-rounded .qtip-titlebar{
	-moz-border-radius: 4px 4px 0 0;
	-webkit-border-radius: 4px 4px 0 0;
	border-radius: 4px 4px 0 0;
}

/* Youtube tooltip style */
.qtip-youtube{
	-moz-border-radius: 2px;
	-webkit-border-radius: 2px;
	border-radius: 2px;

	-webkit-box-shadow: 0 0 3px #333;
	-moz-box-shadow: 0 0 3px #333;
	box-shadow: 0 0 3px #333;

	color: white;
	border: 0 solid transparent;

	background: #4A4A4A;
	background-image: -webkit-gradient(linear,left top,left bottom,color-stop(0,#4A4A4A),color-stop(100%,black));
	background-image: -webkit-linear-gradient(top,#4A4A4A 0,black 100%);
	background-image: -moz-linear-gradient(top,#4A4A4A 0,black 100%);
	background-image: -ms-linear-gradient(top,#4A4A4A 0,black 100%);
	background-image: -o-linear-gradient(top,#4A4A4A 0,black 100%);
}

	.qtip-youtube .qtip-titlebar{
		background-color: #4A4A4A;
		background-color: rgba(0,0,0,0);
	}

	.qtip-youtube .qtip-content{
		padding: .75em;
		font: 12px arial,sans-serif;

		filter: progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#4a4a4a,EndColorStr=#000000);
		-ms-filter: "progid:DXImageTransform.Microsoft.Gradient(GradientType=0,StartColorStr=#4a4a4a,EndColorStr=#000000);";
	}

	.qtip-youtube .qtip-icon{
		border-color: #222;
	}

	.qtip-youtube .qtip-titlebar .ui-state-hover{
		border-color: #303030;
	}


/* jQuery TOOLS Tooltip style */
.qtip-jtools{
	background: #232323;
	background: rgba(0, 0, 0, 0.7);
	background-image: -webkit-gradient(linear, left top, left bottom, from(#717171), to(#232323));
	background-image: -moz-linear-gradient(top, #717171, #232323);
	background-image: -webkit-linear-gradient(top, #717171, #232323);
	background-image: -ms-linear-gradient(top, #717171, #232323);
	background-image: -o-linear-gradient(top, #717171, #232323);

	border: 2px solid #ddd;
	border: 2px solid rgba(241,241,241,1);

	-moz-border-radius: 2px;
	-webkit-border-radius: 2px;
	border-radius: 2px;

	-webkit-box-shadow: 0 0 12px #333;
	-moz-box-shadow: 0 0 12px #333;
	box-shadow: 0 0 12px #333;
}

	/* IE Specific */
	.qtip-jtools .qtip-titlebar{
		background-color: transparent;
		filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=#717171,endColorstr=#4A4A4A);
		-ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr=#717171,endColorstr=#4A4A4A)";
	}
	.qtip-jtools .qtip-content{
		filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=#4A4A4A,endColorstr=#232323);
		-ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr=#4A4A4A,endColorstr=#232323)";
	}

	.qtip-jtools .qtip-titlebar,
	.qtip-jtools .qtip-content{
		background: transparent;
		color: white;
		border: 0 dashed transparent;
	}

	.qtip-jtools .qtip-icon{
		border-color: #555;
	}

	.qtip-jtools .qtip-titlebar .ui-state-hover{
		border-color: #333;
	}


/* Cluetip style */
.qtip-cluetip{
	-webkit-box-shadow: 4px 4px 5px rgba(0, 0, 0, 0.4);
	-moz-box-shadow: 4px 4px 5px rgba(0, 0, 0, 0.4);
	box-shadow: 4px 4px 5px rgba(0, 0, 0, 0.4);

	background-color: #D9D9C2;
	color: #111;
	border: 0 dashed transparent;
}

	.qtip-cluetip .qtip-titlebar{
		background-color: #87876A;
		color: white;
		border: 0 dashed transparent;
	}

	.qtip-cluetip .qtip-icon{
		border-color: #808064;
	}

	.qtip-cluetip .qtip-titlebar .ui-state-hover{
		border-color: #696952;
		color: #696952;
	}


/* Tipsy style */
.qtip-tipsy{
	background: black;
	background: rgba(0, 0, 0, .87);

	color: white;
	border: 0 solid transparent;

	font-size: 11px;
	font-family: 'Lucida Grande', sans-serif;
	font-weight: bold;
	line-height: 16px;
	text-shadow: 0 1px black;
}

	.qtip-tipsy .qtip-titlebar{
		padding: 6px 35px 0 10px;
		background-color: transparent;
	}

	.qtip-tipsy .qtip-content{
		padding: 6px 10px;
	}

	.qtip-tipsy .qtip-icon{
		border-color: #222;
		text-shadow: none;
	}

	.qtip-tipsy .qtip-titlebar .ui-state-hover{
		border-color: #303030;
	}


/* Tipped style */
.qtip-tipped{
	border: 3px solid #959FA9;

	-moz-border-radius: 3px;
	-webkit-border-radius: 3px;
	border-radius: 3px;

	background-color: #F9F9F9;
	color: #454545;

	font-weight: normal;
	font-family: serif;
}

	.qtip-tipped .qtip-titlebar{
		border-bottom-width: 0;

		color: white;
		background: #3A79B8;
		background-image: -webkit-gradient(linear, left top, left bottom, from(#3A79B8), to(#2E629D));
		background-image: -webkit-linear-gradient(top, #3A79B8, #2E629D);
		background-image: -moz-linear-gradient(top, #3A79B8, #2E629D);
		background-image: -ms-linear-gradient(top, #3A79B8, #2E629D);
		background-image: -o-linear-gradient(top, #3A79B8, #2E629D);
		filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=#3A79B8,endColorstr=#2E629D);
		-ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr=#3A79B8,endColorstr=#2E629D)";
	}

	.qtip-tipped .qtip-icon{
		border: 2px solid #285589;
		background: #285589;
	}

		.qtip-tipped .qtip-icon .ui-icon{
			background-color: #FBFBFB;
			color: #555;
		}


/**
 * Twitter Bootstrap style.
 *
 * Tested with IE 8, IE 9, Chrome 18, Firefox 9, Opera 11.
 * Does not work with IE 7.
 */
.qtip-bootstrap{
	/** Taken from Bootstrap body */
	font-size: 14px;
	line-height: 20px;
	color: #333333;

	/** Taken from Bootstrap .popover */
	padding: 1px;
	background-color: #ffffff;
	border: 1px solid #ccc;
	border: 1px solid rgba(0, 0, 0, 0.2);
	-webkit-border-radius: 6px;
	-moz-border-radius: 6px;
	border-radius: 6px;
	-webkit-box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
	-moz-box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
	box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
	-webkit-background-clip: padding-box;
	-moz-background-clip: padding;
	background-clip: padding-box;
}

	.qtip-bootstrap .qtip-titlebar{
		/** Taken from Bootstrap .popover-title */
		padding: 8px 14px;
		margin: 0;
		font-size: 14px;
		font-weight: normal;
		line-height: 18px;
		background-color: #f7f7f7;
		border-bottom: 1px solid #ebebeb;
		-webkit-border-radius: 5px 5px 0 0;
		-moz-border-radius: 5px 5px 0 0;
		border-radius: 5px 5px 0 0;
	}

		.qtip-bootstrap .qtip-titlebar .qtip-close{
			/**
			 * Overrides qTip2:
			 * .qtip-titlebar .qtip-close{
			 *   [...]
			 *   right: 4px;
			 *   top: 50%;
			 *   [...]
			 *   border-style: solid;
			 * }
			 */
			right: 11px;
			top: 45%;
			border-style: none;
		}

	.qtip-bootstrap .qtip-content{
		/** Taken from Bootstrap .popover-content */
		padding: 9px 14px;
	}

	.qtip-bootstrap .qtip-icon{
		/**
		 * Overrides qTip2:
		 * .qtip-default .qtip-icon {
		 *   border-color: #CCC;
		 *   background: #F1F1F1;
		 *   color: #777;
		 * }
		 */
		background: transparent;
	}

		.qtip-bootstrap .qtip-icon .ui-icon{
			/**
			 * Overrides qTip2:
			 * .qtip-icon .ui-icon{
			 *   width: 18px;
			 *   height: 14px;
			 * }
			 */
			width: auto;
			height: auto;

			/* Taken from Bootstrap .close */
			float: right;
			font-size: 20px;
			font-weight: bold;
			line-height: 18px;
			color: #000000;
			text-shadow: 0 1px 0 #ffffff;
			opacity: 0.2;
			filter: alpha(opacity=20);
		}

		.qtip-bootstrap .qtip-icon .ui-icon:hover{
			/* Taken from Bootstrap .close:hover */
			color: #000000;
			text-decoration: none;
			cursor: pointer;
			opacity: 0.4;
			filter: alpha(opacity=40);
		}


/* IE9 fix - removes all filters */
.qtip:not(.ie9haxors) div.qtip-content,
.qtip:not(.ie9haxors) div.qtip-titlebar{
	filter: none;
	-ms-filter: none;
}


.qtip .qtip-tip{
	margin: 0 auto;
	overflow: hidden;
	z-index: 10;

}

	/* Opera bug #357 - Incorrect tip position
	https://github.com/Craga89/qTip2/issues/367 */
	x:-o-prefocus, .qtip .qtip-tip{
		visibility: hidden;
	}

	.qtip .qtip-tip,
	.qtip .qtip-tip .qtip-vml,
	.qtip .qtip-tip canvas{
		position: absolute;

		color: #123456;
		background: transparent;
		border: 0 dashed transparent;
	}

	.qtip .qtip-tip canvas{ top: 0; left: 0; }

	.qtip .qtip-tip .qtip-vml{
		behavior: url("/wiki/extensions/SemanticMediaWiki/res/jquery/#default#VML");
		display: inline-block;
		visibility: visible;
	}

/*!
 * This file is part of the Semantic MediaWiki Tooltip/Highlighter module
 * @see https://semantic-mediawiki.org/
 *
 * @section LICENSE
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 * http://www.gnu.org/copyleft/gpl.html
 *
 * @since 1.8
 *
 * @file
 * @ingroup SMW
 *
 * @licence GNU GPL v2+
 * @author mwjames
 */

/* Tooltips, style for content of the bubble */
div.smwtt {
	color: #000000;
}

/* Tooltips, show persistent tooltips for non-JavaScript clients */
span.smwttpersist span.smwttcontent {
	color: #888888;
	font-style: italic;
	font-size: 90%;
}

/* Tooltips, hide inline tooltips for non-JavaScript clients */
span.smwttinline span.smwttcontent {
	display: none;
	speak: none;
}

/* Tooltips, style for image anchor for persistent tooltips */
span.smwtticon {
	display: none;
}

/* Tooltips, colored anchors? */
span.smwttactivepersist {
	cursor: help;
	color: #0000C8;
}

/* Tooltips, colored anchors */
span.smwttactiveinline {
	color: #BB7700;
	text-decoration: none;
}

/* Tooltips, images for tooltip icons */
img.smwttimg {
	padding-right: 5px;
	padding-left: 4px;
}

/* New tooltip content is always hidden */
.smwttcontent {
	display:none;
}

/* New tooltip icon defaults */
.smwtticon {
	padding:14px 12px 0 0;
	white-space:nowrap;
	margin-bottom: -1px;
}

/* New tooltip, Individual assigned icons ( inline-block is important because the icon <span> is empty) */
.smwtticon.info {
	display:inline-block;
	background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAB+klEQVR4AWJkgANxNo3APFVNRVENNmYGBaDA/1+/GR5cvffi+q1NE+4wMLz7DVIF0SBmK2IbnhvjaaUcLy4mrCYIaFqaAbaKAuh5795n/ba1ZNt27WFqyfbanI0tT9m2bX+2zYyD5UBTpDyAQCgSszu9b0/d/Lj31pH1B+C+7SMoG2gMnzZ/+aSRPZZ2aC2vH9WpjGutkJi2cokReIFXDK2yrKy4b0qtZ798tDwgHaYsmtSnX++1VWWKVlUoIpwErnwII50DOtVKeG6LIccyIsMrXSJQn1JKmSG8qiq+RB73rUkQmgHLENQW8sjkAHsUiH3vBM3QOQ6DaSiN4jfeDGpAUGxQ8ITDjA4iiiQWWx/GEUix8IYAkyeDYAqlFITPRPI8LHGCqCSg5Lt1keCJD/iUEhFNAd54ElFwYAlNU2SSbwXK5hVVYjRNQKlG8CIIuNNAiU4ACEgmJaSTkVw+k37NRtzmMyG76Z2hCDBkgnIV6FwEVCKBcgXQZQpDFRGymV6HnV/Ok+inW84oVFNOKGyrrygor9B5plpl8NKWQJ7j4PKEsw9uPX745sL+Nb5rm24y+AVitB/WtcPY2TPbakrb15fIpdk88NUTdb0xO5+/OLZpZ/TdtacAsgz+g1xcX1DZ0qWySC8s/37I+0Nep+PDI3vcZwniN74BNcHHQEW4ECsAAAAASUVORK5CYII=) no-repeat left bottom;
	background: url(/wiki/extensions/SemanticMediaWiki/res/images/info.png?7fa1d) no-repeat left bottom!ie;
}

.smwtticon.service {
	display:inline-block;
	background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAB+klEQVR4AWJkgANxNo3APFVNRVENNmYGBaDA/1+/GR5cvffi+q1NE+4wMLz7DVIF0SBmK2IbnhvjaaUcLy4mrCYIaFqaAbaKAuh5795n/ba1ZNt27WFqyfbanI0tT9m2bX+2zYyD5UBTpDyAQCgSszu9b0/d/Lj31pH1B+C+7SMoG2gMnzZ/+aSRPZZ2aC2vH9WpjGutkJi2cokReIFXDK2yrKy4b0qtZ798tDwgHaYsmtSnX++1VWWKVlUoIpwErnwII50DOtVKeG6LIccyIsMrXSJQn1JKmSG8qiq+RB73rUkQmgHLENQW8sjkAHsUiH3vBM3QOQ6DaSiN4jfeDGpAUGxQ8ITDjA4iiiQWWx/GEUix8IYAkyeDYAqlFITPRPI8LHGCqCSg5Lt1keCJD/iUEhFNAd54ElFwYAlNU2SSbwXK5hVVYjRNQKlG8CIIuNNAiU4ACEgmJaSTkVw+k37NRtzmMyG76Z2hCDBkgnIV6FwEVCKBcgXQZQpDFRGymV6HnV/Ok+inW84oVFNOKGyrrygor9B5plpl8NKWQJ7j4PKEsw9uPX745sL+Nb5rm24y+AVitB/WtcPY2TPbakrb15fIpdk88NUTdb0xO5+/OLZpZ/TdtacAsgz+g1xcX1DZ0qWySC8s/37I+0Nep+PDI3vcZwniN74BNcHHQEW4ECsAAAAASUVORK5CYII=) no-repeat left bottom;
	background: url(/wiki/extensions/SemanticMediaWiki/res/images/info.png?7fa1d) no-repeat left bottom!ie;
}

.smwtticon.warning {
	display:inline-block;
	background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAABfUlEQVR4AZXLs6IdYRRA4fXPHGtm7rGu7Tsntm3bNrq0aePkBVLmJWLbtlHG3LG9NrqPH9vVjqoDfVk5v4g6fkhE0PimHTb+YFKbWtwvPLNfrTbL9hPih76ArU3gDqqmSNu6gb4+a/wlnWr6TixRLSs9qF8ClxefWRue+6i6a+n6TdeR6i4FtTlrbvMwwV8Ch1trHsqV9b34LMGevYc59ThKbbvSbsmg1u4nsN3GCJR4l4Z7dwyaEQ9Ox0uMsItI31b+wS3cCzsEiX0BO210X5QhicGZdno8im2/oKJCp3nzJ6iYl4rh4ZZjqhma0HF+AJqDlNXSOcKfS5lwFpFT9O3rAE4Cpwk2N0K5zvrw8RkyH0CwmmFWF09nZ/Segn0cOryPSZO3sGPnQeAYevSBquitt6trZByAIxBTs4Lpl265exOA0pCwbPprqvIeIbffAK/xp944qwqZCixXG3uwIZTVikWUAj5+JfBGkDcAglKoG1d4MH+LTFAiwv/0FhheYpPzYQn1AAAAAElFTkSuQmCC) no-repeat left bottom;
	background: url(/wiki/extensions/SemanticMediaWiki/res/images/warning.png?12984) no-repeat left bottom!ie;
}

.smwtticon.note {
	display:inline-block;
	background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAB7ElEQVR4ASWNM9hcTQCF35m9e9efbSx+22bSxEnfpI6TMmX6J0YVdbGNJrZtY82rmeiwO0dowIuY3Jv8NXZAtWEExhqB0DeuNL1c90+n7J5vtlVEMBPv7yGZTGIACEehpBjZNJBY0NCXSJqRGEiTWqnI0wd7Lt/0D08T8fhBAKP8++dYMflf+5fJnfVdfRIhobEXhCDs9xNv7fgscP7EnvSd3rHVzvadxtMfQm2xntYVHfWmVKXX4A8jPxvN23n00aVghun99Asje2rbikuxri/l8dY/x9XHfIO6kgfrravpty6grbeuZqBWAKdMb3OwO3Pj9EQjEgqlDG2jHAXSALsMbvVD13JoAOUQNsGff/2rYTnOY21XUNpESAOUi07fAasIdgGEAGW/f1SqLWI8TpfPW40lQtEQWhggJN6ZVYBAeB7YJaTwKKZf4rT+fkd++fvI80/d1qvCyqOdGtou4xs5D9/vM9DVHLgWlF5xt2Aq0RbfKJ48f0Hx3qVfwztnHOyqs03tD0LfzwjlIV5dR6C4/qjG0x/mLOz7/MepQmuNBxxev2ZE27W1Szq8e8MhUQNpUFZhHtDnPYtPWvzpb//Piff32gaAdl1UU+/eV3/M/e7ly9sTRPbhLwqiTrTrjmyLb/E51knh2gC8AXng4FD0wz3SAAAAAElFTkSuQmCC) no-repeat left bottom;
	background: url(/wiki/extensions/SemanticMediaWiki/res/images/note.png?b4186) no-repeat left bottom!ie;
}