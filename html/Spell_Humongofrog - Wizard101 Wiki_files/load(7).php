/**
 * Code in this file MUST work on even the most ancient of browsers!
 *
 * This file is where we decide whether to initialise the modern run-time.
 */
/*jshint unused: false */
/*globals mw, RLQ: true, NORLQ: true, $VARS, $CODE, performance */

var mediaWikiLoadStart = ( new Date() ).getTime(),

	mwPerformance = ( window.performance && performance.mark ) ? performance : {
		mark: function () {}
	};

mwPerformance.mark( 'mwLoadStart' );

/**
 * See <https://www.mediawiki.org/wiki/Compatibility#Browsers>
 *
 * Capabilities required for modern run-time:
 * - DOM Level 4 & Selectors API Level 1
 * - HTML5 & Web Storage
 * - DOM Level 2 Events
 *
 * Browsers we support in our modern run-time (Grade A):
 * - Chrome
 * - IE 9+
 * - Firefox 3.5+
 * - Safari 4+
 * - Opera 10.5+
 * - Mobile Safari (iOS 1+)
 * - Android 2.0+
 *
 * Browsers we support in our no-javascript run-time (Grade C):
 * - IE 6+
 * - Firefox 3+
 * - Safari 3+
 * - Opera 10+
 * - WebOS < 1.5
 * - PlayStation
 * - Symbian-based browsers
 * - NetFront-based browser
 * - Opera Mini
 * - Nokia's Ovi Browser
 * - MeeGo's browser
 * - Google Glass
 *
 * Other browsers that pass the check are considered Grade X.
 */
function isCompatible( str ) {
	var ua = str || navigator.userAgent;
	return !!(
		// http://caniuse.com/#feat=queryselector
		'querySelector' in document

		// http://caniuse.com/#feat=namevalue-storage
		// https://developer.blackberry.com/html5/apis/v1_0/localstorage.html
		// https://blog.whatwg.org/this-week-in-html-5-episode-30
		&& 'localStorage' in window

		// http://caniuse.com/#feat=addeventlistener
		&& 'addEventListener' in window

		// Hardcoded exceptions for browsers that pass the requirement but we don't want to
		// support in the modern run-time.
		&& !(
			ua.match( /webOS\/1\.[0-4]/ ) ||
			ua.match( /PlayStation/i ) ||
			ua.match( /SymbianOS|Series60|NetFront|Opera Mini|S40OviBrowser|MeeGo/ ) ||
			( ua.match( /Glass/ ) && ua.match( /Android/ ) )
		)
	);
}

// Conditional script injection
( function () {
	var NORLQ, script;
	if ( !isCompatible() ) {
		// Undo class swapping in case of an unsupported browser.
		// See ResourceLoaderClientHtml::getDocumentAttributes().
		document.documentElement.className = document.documentElement.className
			.replace( /(^|\s)client-js(\s|$)/, '$1client-nojs$2' );

		NORLQ = window.NORLQ || [];
		while ( NORLQ.length ) {
			NORLQ.shift()();
		}
		window.NORLQ = {
			push: function ( fn ) {
				fn();
			}
		};

		// Clear and disable the other queue
		window.RLQ = {
			// No-op
			push: function () {}
		};

		return;
	}

	/**
	 * The $CODE and $VARS placeholders are substituted in ResourceLoaderStartUpModule.php.
	 */
	function startUp() {
		mw.config = new mw.Map( true );

		mw.loader.addSource( {
	    "local": "/wiki/load.php"
	} );
	mw.loader.register( [
	    [
	        "site",
	        "1wdmv5v",
	        [
	            1
	        ]
	    ],
	    [
	        "site.styles",
	        "1f6n0lg",
	        [],
	        "site"
	    ],
	    [
	        "noscript",
	        "1cwl9at",
	        [],
	        "noscript"
	    ],
	    [
	        "filepage",
	        "09ej4na"
	    ],
	    [
	        "user.groups",
	        "0b214ac",
	        [
	            5
	        ]
	    ],
	    [
	        "user",
	        "1lttinc",
	        [
	            6
	        ],
	        "user"
	    ],
	    [
	        "user.styles",
	        "0r4yndy",
	        [],
	        "user"
	    ],
	    [
	        "user.cssprefs",
	        "09p30q0",
	        [],
	        "private"
	    ],
	    [
	        "user.defaults",
	        "16kkoc2"
	    ],
	    [
	        "user.options",
	        "0wwfj8s",
	        [
	            8
	        ],
	        "private"
	    ],
	    [
	        "user.tokens",
	        "048xc1o",
	        [],
	        "private"
	    ],
	    [
	        "mediawiki.language.data",
	        "00q9h2s",
	        [
	            179
	        ]
	    ],
	    [
	        "mediawiki.skinning.elements",
	        "1d3x4uv"
	    ],
	    [
	        "mediawiki.skinning.content",
	        "0vlvl8e"
	    ],
	    [
	        "mediawiki.skinning.interface",
	        "0mhchkv"
	    ],
	    [
	        "mediawiki.skinning.content.parsoid",
	        "1k1db4x"
	    ],
	    [
	        "mediawiki.skinning.content.externallinks",
	        "0ioei5h"
	    ],
	    [
	        "jquery.accessKeyLabel",
	        "0ldlobp",
	        [
	            27,
	            136
	        ]
	    ],
	    [
	        "jquery.appear",
	        "1dipumj"
	    ],
	    [
	        "jquery.arrowSteps",
	        "0hwk6w6"
	    ],
	    [
	        "jquery.async",
	        "1qu9myr"
	    ],
	    [
	        "jquery.autoEllipsis",
	        "16gluxt",
	        [
	            39
	        ]
	    ],
	    [
	        "jquery.badge",
	        "0h8l9la",
	        [
	            176
	        ]
	    ],
	    [
	        "jquery.byteLength",
	        "0g2qthq"
	    ],
	    [
	        "jquery.byteLimit",
	        "1vhzb6p",
	        [
	            23
	        ]
	    ],
	    [
	        "jquery.checkboxShiftClick",
	        "0v8yz45"
	    ],
	    [
	        "jquery.chosen",
	        "00xh81d"
	    ],
	    [
	        "jquery.client",
	        "1tz3s94"
	    ],
	    [
	        "jquery.color",
	        "0j7hwxp",
	        [
	            29
	        ]
	    ],
	    [
	        "jquery.colorUtil",
	        "1oxpk01"
	    ],
	    [
	        "jquery.confirmable",
	        "19y6zse",
	        [
	            180
	        ]
	    ],
	    [
	        "jquery.cookie",
	        "0li4rh8"
	    ],
	    [
	        "jquery.expandableField",
	        "1pcs3ql"
	    ],
	    [
	        "jquery.farbtastic",
	        "1lmwwjg",
	        [
	            29
	        ]
	    ],
	    [
	        "jquery.footHovzer",
	        "1678tno"
	    ],
	    [
	        "jquery.form",
	        "1p7qei1"
	    ],
	    [
	        "jquery.fullscreen",
	        "175ap99"
	    ],
	    [
	        "jquery.getAttrs",
	        "0wr62py"
	    ],
	    [
	        "jquery.hidpi",
	        "1gw453r"
	    ],
	    [
	        "jquery.highlightText",
	        "0w3jlxz",
	        [
	            251,
	            136
	        ]
	    ],
	    [
	        "jquery.hoverIntent",
	        "1bkbpxj"
	    ],
	    [
	        "jquery.i18n",
	        "08d2kme",
	        [
	            178
	        ]
	    ],
	    [
	        "jquery.localize",
	        "0g1af55"
	    ],
	    [
	        "jquery.makeCollapsible",
	        "0bewdiw"
	    ],
	    [
	        "jquery.mockjax",
	        "0joh7c0"
	    ],
	    [
	        "jquery.mw-jump",
	        "1az9hci"
	    ],
	    [
	        "jquery.mwExtension",
	        "0jt2qem"
	    ],
	    [
	        "jquery.placeholder",
	        "02canxd"
	    ],
	    [
	        "jquery.qunit",
	        "0mouo6s"
	    ],
	    [
	        "jquery.qunit.completenessTest",
	        "136a6b8",
	        [
	            48
	        ]
	    ],
	    [
	        "jquery.spinner",
	        "11mqyuj"
	    ],
	    [
	        "jquery.jStorage",
	        "0zgxkk9",
	        [
	            94
	        ]
	    ],
	    [
	        "jquery.suggestions",
	        "04crf7e",
	        [
	            39
	        ]
	    ],
	    [
	        "jquery.tabIndex",
	        "16kuvyz"
	    ],
	    [
	        "jquery.tablesorter",
	        "1k3eilj",
	        [
	            251,
	            136,
	            181
	        ]
	    ],
	    [
	        "jquery.textSelection",
	        "0zywvdw",
	        [
	            27
	        ]
	    ],
	    [
	        "jquery.throttle-debounce",
	        "0gd74e8"
	    ],
	    [
	        "jquery.xmldom",
	        "0om4srv"
	    ],
	    [
	        "jquery.tipsy",
	        "1xp67uu"
	    ],
	    [
	        "jquery.ui.core",
	        "12sgbem",
	        [
	            60
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.core.styles",
	        "0x22ju2",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.accordion",
	        "0eg58tc",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.autocomplete",
	        "11rzsl5",
	        [
	            68
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.button",
	        "1voybp4",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.datepicker",
	        "0x0eft3",
	        [
	            59
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.dialog",
	        "0sd5gx3",
	        [
	            63,
	            66,
	            70,
	            72
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.draggable",
	        "0hb6hxi",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.droppable",
	        "0sn0etv",
	        [
	            66
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.menu",
	        "042tw2u",
	        [
	            59,
	            70,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.mouse",
	        "1e2rf3a",
	        [
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.position",
	        "0up5uov",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.progressbar",
	        "166iq9c",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.resizable",
	        "1etkx6x",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.selectable",
	        "134nefa",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.slider",
	        "014ttzu",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.sortable",
	        "04r6a3q",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.spinner",
	        "08f2oj2",
	        [
	            63
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.tabs",
	        "0pr77f1",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.tooltip",
	        "0m42un1",
	        [
	            59,
	            70,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.widget",
	        "15g1m19",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.core",
	        "087vbp5",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.blind",
	        "0f117mw",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.bounce",
	        "0okxvbg",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.clip",
	        "1pt2wvx",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.drop",
	        "1tv6idt",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.explode",
	        "16wqtoy",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.fade",
	        "0vf6fnc",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.fold",
	        "12pdmss",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.highlight",
	        "02m06pq",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.pulsate",
	        "0ao9b1a",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.scale",
	        "0avhvtm",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.shake",
	        "1fnq76h",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.slide",
	        "0eapkhi",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.transfer",
	        "0hdx39w",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "json",
	        "1ctfu25",
	        [],
	        null,
	        null,
	        "/*!\n * Skip function for json2.js.\n */\nreturn !!( window.JSON \u0026\u0026 JSON.stringify \u0026\u0026 JSON.parse );\n"
	    ],
	    [
	        "moment",
	        "0swqitb",
	        [
	            176
	        ]
	    ],
	    [
	        "mediawiki.apihelp",
	        "0pusk3v"
	    ],
	    [
	        "mediawiki.template",
	        "0mqyze1"
	    ],
	    [
	        "mediawiki.template.mustache",
	        "1ppbqrj",
	        [
	            97
	        ]
	    ],
	    [
	        "mediawiki.template.regexp",
	        "14gocov",
	        [
	            97
	        ]
	    ],
	    [
	        "mediawiki.apipretty",
	        "1yciyjr"
	    ],
	    [
	        "mediawiki.api",
	        "0z3uenc",
	        [
	            153,
	            10
	        ]
	    ],
	    [
	        "mediawiki.api.category",
	        "0i5l5hk",
	        [
	            141,
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.edit",
	        "0o816c2",
	        [
	            141,
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.login",
	        "0c42mws",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.options",
	        "1x2iojv",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.parse",
	        "1ylax21",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.upload",
	        "19teuvh",
	        [
	            251,
	            94,
	            103
	        ]
	    ],
	    [
	        "mediawiki.api.user",
	        "1rarrwq",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.watch",
	        "09484q7",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.messages",
	        "1qmch7u",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.rollback",
	        "1d0mvxo",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.content.json",
	        "19bjvhh"
	    ],
	    [
	        "mediawiki.confirmCloseWindow",
	        "0y9gs5x"
	    ],
	    [
	        "mediawiki.debug",
	        "12gwtho",
	        [
	            34
	        ]
	    ],
	    [
	        "mediawiki.diff.styles",
	        "1v1esf8"
	    ],
	    [
	        "mediawiki.feedback",
	        "13s4c5x",
	        [
	            141,
	            130,
	            260
	        ]
	    ],
	    [
	        "mediawiki.feedlink",
	        "0u67xra"
	    ],
	    [
	        "mediawiki.filewarning",
	        "1jut26x",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.ForeignApi",
	        "1o8sho6",
	        [
	            120
	        ]
	    ],
	    [
	        "mediawiki.ForeignApi.core",
	        "0s5cbyh",
	        [
	            101,
	            252
	        ]
	    ],
	    [
	        "mediawiki.helplink",
	        "0y5imxk"
	    ],
	    [
	        "mediawiki.hidpi",
	        "1rc7t6w",
	        [
	            38
	        ],
	        null,
	        null,
	        "/*!\n * Skip function for mediawiki.hdpi.js.\n */\nreturn 'srcset' in new Image();\n"
	    ],
	    [
	        "mediawiki.hlist",
	        "1mvlacb"
	    ],
	    [
	        "mediawiki.htmlform",
	        "1i8vx2l",
	        [
	            24,
	            136
	        ]
	    ],
	    [
	        "mediawiki.htmlform.ooui",
	        "029dxig",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.htmlform.styles",
	        "0az1elg"
	    ],
	    [
	        "mediawiki.htmlform.ooui.styles",
	        "18fceaz"
	    ],
	    [
	        "mediawiki.icon",
	        "0yah39a"
	    ],
	    [
	        "mediawiki.inspect",
	        "1hfq68l",
	        [
	            23,
	            94,
	            136
	        ]
	    ],
	    [
	        "mediawiki.messagePoster",
	        "0h1ajcm",
	        [
	            119
	        ]
	    ],
	    [
	        "mediawiki.messagePoster.wikitext",
	        "1bg5fuk",
	        [
	            103,
	            130
	        ]
	    ],
	    [
	        "mediawiki.notification",
	        "1h1wy8q",
	        [
	            189
	        ]
	    ],
	    [
	        "mediawiki.notify",
	        "1p3fe9c"
	    ],
	    [
	        "mediawiki.notification.convertmessagebox",
	        "1nkcu0t",
	        [
	            132
	        ]
	    ],
	    [
	        "mediawiki.notification.convertmessagebox.styles",
	        "1ubcalq"
	    ],
	    [
	        "mediawiki.RegExp",
	        "0ghj84m"
	    ],
	    [
	        "mediawiki.pager.tablePager",
	        "0w4d71a"
	    ],
	    [
	        "mediawiki.searchSuggest",
	        "1vqva5s",
	        [
	            37,
	            47,
	            52,
	            101
	        ]
	    ],
	    [
	        "mediawiki.sectionAnchor",
	        "0u2zxnc"
	    ],
	    [
	        "mediawiki.storage",
	        "1y2qdea"
	    ],
	    [
	        "mediawiki.Title",
	        "0cd9odx",
	        [
	            23,
	            153
	        ]
	    ],
	    [
	        "mediawiki.Upload",
	        "19cse43",
	        [
	            107
	        ]
	    ],
	    [
	        "mediawiki.ForeignUpload",
	        "18onl4g",
	        [
	            119,
	            142
	        ]
	    ],
	    [
	        "mediawiki.ForeignStructuredUpload.config",
	        "0xf06i9"
	    ],
	    [
	        "mediawiki.ForeignStructuredUpload",
	        "0uldiaz",
	        [
	            144,
	            143
	        ]
	    ],
	    [
	        "mediawiki.Upload.Dialog",
	        "1jxydcs",
	        [
	            147
	        ]
	    ],
	    [
	        "mediawiki.Upload.BookletLayout",
	        "0vl8yqk",
	        [
	            142,
	            180,
	            151,
	            249,
	            95,
	            258,
	            260,
	            266,
	            267
	        ]
	    ],
	    [
	        "mediawiki.ForeignStructuredUpload.BookletLayout",
	        "1erfzpa",
	        [
	            145,
	            147,
	            110,
	            184,
	            245,
	            243
	        ]
	    ],
	    [
	        "mediawiki.toc",
	        "13lm3n2",
	        [
	            157
	        ]
	    ],
	    [
	        "mediawiki.Uri",
	        "0ejn0vr",
	        [
	            153,
	            99
	        ]
	    ],
	    [
	        "mediawiki.user",
	        "1hgi164",
	        [
	            108,
	            157,
	            9
	        ]
	    ],
	    [
	        "mediawiki.userSuggest",
	        "0oq6adb",
	        [
	            52,
	            101
	        ]
	    ],
	    [
	        "mediawiki.util",
	        "1d01z4k",
	        [
	            17,
	            133
	        ]
	    ],
	    [
	        "mediawiki.viewport",
	        "12yfsj8"
	    ],
	    [
	        "mediawiki.checkboxtoggle",
	        "1ybr8k9"
	    ],
	    [
	        "mediawiki.checkboxtoggle.styles",
	        "1wadpb1"
	    ],
	    [
	        "mediawiki.cookie",
	        "1rk07py",
	        [
	            31
	        ]
	    ],
	    [
	        "mediawiki.toolbar",
	        "0q9rfrz",
	        [
	            55
	        ]
	    ],
	    [
	        "mediawiki.experiments",
	        "0gqg3zs"
	    ],
	    [
	        "mediawiki.action.edit",
	        "078syrs",
	        [
	            24,
	            55,
	            161,
	            101
	        ]
	    ],
	    [
	        "mediawiki.action.edit.styles",
	        "0wpjn9j"
	    ],
	    [
	        "mediawiki.action.edit.collapsibleFooter",
	        "0anmy91",
	        [
	            43,
	            157,
	            128
	        ]
	    ],
	    [
	        "mediawiki.action.edit.preview",
	        "0dcwx3u",
	        [
	            35,
	            50,
	            55,
	            101,
	            115,
	            180
	        ]
	    ],
	    [
	        "mediawiki.action.history",
	        "1idfqg1"
	    ],
	    [
	        "mediawiki.action.history.styles",
	        "1tkodnx"
	    ],
	    [
	        "mediawiki.action.history.diff",
	        "1v1esf8"
	    ],
	    [
	        "mediawiki.action.view.dblClickEdit",
	        "06vcdqa",
	        [
	            189,
	            9
	        ]
	    ],
	    [
	        "mediawiki.action.view.metadata",
	        "1bsrnie"
	    ],
	    [
	        "mediawiki.action.view.categoryPage.styles",
	        "0lftsa5"
	    ],
	    [
	        "mediawiki.action.view.postEdit",
	        "1fr3pby",
	        [
	            157,
	            180,
	            97
	        ]
	    ],
	    [
	        "mediawiki.action.view.redirect",
	        "1rev9lr",
	        [
	            27
	        ]
	    ],
	    [
	        "mediawiki.action.view.redirectPage",
	        "10l47k7"
	    ],
	    [
	        "mediawiki.action.view.rightClickEdit",
	        "0clt0ou"
	    ],
	    [
	        "mediawiki.action.edit.editWarning",
	        "10te9z2",
	        [
	            55,
	            113,
	            180
	        ]
	    ],
	    [
	        "mediawiki.action.view.filepage",
	        "1pz3v8y"
	    ],
	    [
	        "mediawiki.language",
	        "08yatiu",
	        [
	            177,
	            11
	        ]
	    ],
	    [
	        "mediawiki.cldr",
	        "1933u29",
	        [
	            178
	        ]
	    ],
	    [
	        "mediawiki.libs.pluralruleparser",
	        "0f14q5j"
	    ],
	    [
	        "mediawiki.language.init",
	        "14rp6t6"
	    ],
	    [
	        "mediawiki.jqueryMsg",
	        "0jm4mo7",
	        [
	            251,
	            176,
	            153,
	            9
	        ]
	    ],
	    [
	        "mediawiki.language.months",
	        "0ing44d",
	        [
	            176
	        ]
	    ],
	    [
	        "mediawiki.language.names",
	        "08qooga",
	        [
	            179
	        ]
	    ],
	    [
	        "mediawiki.language.specialCharacters",
	        "1mgfjmk",
	        [
	            176
	        ]
	    ],
	    [
	        "mediawiki.libs.jpegmeta",
	        "04wx8ua"
	    ],
	    [
	        "mediawiki.page.gallery",
	        "0z3ezu5",
	        [
	            56,
	            186
	        ]
	    ],
	    [
	        "mediawiki.page.gallery.styles",
	        "04vzu27"
	    ],
	    [
	        "mediawiki.page.gallery.slideshow",
	        "13d03rd",
	        [
	            141,
	            101,
	            258,
	            274
	        ]
	    ],
	    [
	        "mediawiki.page.ready",
	        "19d7we1",
	        [
	            17,
	            25,
	            43,
	            45,
	            47
	        ]
	    ],
	    [
	        "mediawiki.page.startup",
	        "0o0x8x0",
	        [
	            153
	        ]
	    ],
	    [
	        "mediawiki.page.patrol.ajax",
	        "10312d8",
	        [
	            50,
	            141,
	            101,
	            189
	        ]
	    ],
	    [
	        "mediawiki.page.watch.ajax",
	        "1tzzskk",
	        [
	            109,
	            189
	        ]
	    ],
	    [
	        "mediawiki.page.rollback",
	        "1tpempm",
	        [
	            50,
	            111
	        ]
	    ],
	    [
	        "mediawiki.page.image.pagination",
	        "1ffezmz",
	        [
	            50,
	            153
	        ]
	    ],
	    [
	        "mediawiki.special",
	        "0vewl2j"
	    ],
	    [
	        "mediawiki.special.apisandbox.styles",
	        "16gfzuv"
	    ],
	    [
	        "mediawiki.special.apisandbox",
	        "15i9v4w",
	        [
	            101,
	            180,
	            244,
	            255
	        ]
	    ],
	    [
	        "mediawiki.special.block",
	        "0v0d1ae",
	        [
	            153
	        ]
	    ],
	    [
	        "mediawiki.special.changeslist",
	        "0oihyq6"
	    ],
	    [
	        "mediawiki.special.changeslist.legend",
	        "0mj16pj"
	    ],
	    [
	        "mediawiki.special.changeslist.legend.js",
	        "1rm4qwh",
	        [
	            43,
	            157
	        ]
	    ],
	    [
	        "mediawiki.special.changeslist.enhanced",
	        "0fq536i"
	    ],
	    [
	        "mediawiki.special.changeslist.visitedstatus",
	        "1tna4qn"
	    ],
	    [
	        "mediawiki.special.comparepages.styles",
	        "0mzmc27"
	    ],
	    [
	        "mediawiki.special.edittags",
	        "0nl8tpy",
	        [
	            26
	        ]
	    ],
	    [
	        "mediawiki.special.edittags.styles",
	        "1feza0t"
	    ],
	    [
	        "mediawiki.special.import",
	        "0odszmo"
	    ],
	    [
	        "mediawiki.special.movePage",
	        "1ghcdmx",
	        [
	            241
	        ]
	    ],
	    [
	        "mediawiki.special.movePage.styles",
	        "001tq9t"
	    ],
	    [
	        "mediawiki.special.pageLanguage",
	        "18hx6cd",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.special.pagesWithProp",
	        "1jtm5hq"
	    ],
	    [
	        "mediawiki.special.preferences",
	        "0v10o86",
	        [
	            113,
	            176,
	            134
	        ]
	    ],
	    [
	        "mediawiki.special.userrights",
	        "1hs26s1",
	        [
	            134
	        ]
	    ],
	    [
	        "mediawiki.special.preferences.styles",
	        "1oi9w01"
	    ],
	    [
	        "mediawiki.special.recentchanges",
	        "07ze2dp"
	    ],
	    [
	        "mediawiki.special.search",
	        "03u2hie",
	        [
	            247
	        ]
	    ],
	    [
	        "mediawiki.special.search.styles",
	        "0wbs3r9"
	    ],
	    [
	        "mediawiki.special.undelete",
	        "0k6ck9c"
	    ],
	    [
	        "mediawiki.special.upload",
	        "16iuka4",
	        [
	            50,
	            141,
	            101,
	            113,
	            180,
	            184,
	            219,
	            97
	        ]
	    ],
	    [
	        "mediawiki.special.upload.styles",
	        "0tamecg"
	    ],
	    [
	        "mediawiki.special.userlogin.common.styles",
	        "0bs9na4"
	    ],
	    [
	        "mediawiki.special.userlogin.signup.styles",
	        "17gjn45"
	    ],
	    [
	        "mediawiki.special.userlogin.login.styles",
	        "0qx1qz4"
	    ],
	    [
	        "mediawiki.special.userlogin.signup.js",
	        "1qvhs39",
	        [
	            56,
	            101,
	            180
	        ]
	    ],
	    [
	        "mediawiki.special.unwatchedPages",
	        "10q1lx2",
	        [
	            141,
	            109
	        ]
	    ],
	    [
	        "mediawiki.special.watchlist",
	        "0yrjt8s"
	    ],
	    [
	        "mediawiki.special.version",
	        "1du7al6"
	    ],
	    [
	        "mediawiki.legacy.config",
	        "12x9bdv"
	    ],
	    [
	        "mediawiki.legacy.commonPrint",
	        "1uaxse3"
	    ],
	    [
	        "mediawiki.legacy.protect",
	        "17ii5cf",
	        [
	            24
	        ]
	    ],
	    [
	        "mediawiki.legacy.shared",
	        "175emkk"
	    ],
	    [
	        "mediawiki.legacy.oldshared",
	        "08j8txo"
	    ],
	    [
	        "mediawiki.legacy.wikibits",
	        "1q0lukc",
	        [
	            153
	        ]
	    ],
	    [
	        "mediawiki.ui",
	        "1g8vowz"
	    ],
	    [
	        "mediawiki.ui.checkbox",
	        "0a057tk"
	    ],
	    [
	        "mediawiki.ui.radio",
	        "1flclsp"
	    ],
	    [
	        "mediawiki.ui.anchor",
	        "1prk5da"
	    ],
	    [
	        "mediawiki.ui.button",
	        "0kiotn0"
	    ],
	    [
	        "mediawiki.ui.input",
	        "0blg1zd"
	    ],
	    [
	        "mediawiki.ui.icon",
	        "0uouv6u"
	    ],
	    [
	        "mediawiki.ui.text",
	        "10z4vml"
	    ],
	    [
	        "mediawiki.widgets",
	        "0pcryd0",
	        [
	            21,
	            24,
	            141,
	            101,
	            242,
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.styles",
	        "1a5jn2f"
	    ],
	    [
	        "mediawiki.widgets.DateInputWidget",
	        "13t2zwd",
	        [
	            95,
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.datetime",
	        "0ulchpu",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.widgets.CategorySelector",
	        "0zzz0rj",
	        [
	            119,
	            141,
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.UserInputWidget",
	        "1c49z9d",
	        [
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.SearchInputWidget",
	        "1lu652n",
	        [
	            138,
	            241
	        ]
	    ],
	    [
	        "mediawiki.widgets.SearchInputWidget.styles",
	        "1n2psnh"
	    ],
	    [
	        "mediawiki.widgets.StashedFileWidget",
	        "0bsxkf7",
	        [
	            256
	        ]
	    ],
	    [
	        "es5-shim",
	        "1h6h1o7",
	        [],
	        null,
	        null,
	        "/*!\n * Skip function for es5-shim module.\n *\n * Test for strict mode as a proxy for full ES5 function support (but not syntax)\n * Per http://kangax.github.io/compat-table/es5/ this is a reasonable shortcut\n * that still allows this to be as short as possible (there are no browsers we\n * support that have strict mode, but lack other features).\n *\n * Do explicitly test for Function#bind because of PhantomJS (which implements\n * strict mode, but lacks Function#bind).\n *\n * IE9 supports all features except strict mode, so loading es5-shim should be close to\n * a no-op but does increase page payload).\n */\nreturn ( function () {\n\t'use strict';\n\treturn !this \u0026\u0026 !!Function.prototype.bind;\n}() );\n"
	    ],
	    [
	        "dom-level2-shim",
	        "184bj15",
	        [],
	        null,
	        null,
	        "/*!\n * Skip function for dom-level2-shim module.\n *\n * Tests for window.Node because that's the only thing that this shim is adding.\n */\nreturn !!window.Node;\n"
	    ],
	    [
	        "oojs",
	        "0fqc02o",
	        [
	            250,
	            94
	        ]
	    ],
	    [
	        "mediawiki.router",
	        "0sbdrif",
	        [
	            254
	        ]
	    ],
	    [
	        "oojs-router",
	        "148dgjx",
	        [
	            252
	        ]
	    ],
	    [
	        "oojs-ui",
	        "0b214ac",
	        [
	            259,
	            258,
	            260
	        ]
	    ],
	    [
	        "oojs-ui-core",
	        "1hth5vj",
	        [
	            176,
	            252,
	            257,
	            261,
	            262,
	            263
	        ]
	    ],
	    [
	        "oojs-ui-core.styles",
	        "0wg6n04"
	    ],
	    [
	        "oojs-ui-widgets",
	        "1gsbu3v",
	        [
	            256
	        ]
	    ],
	    [
	        "oojs-ui-toolbars",
	        "0gcq6p2",
	        [
	            256
	        ]
	    ],
	    [
	        "oojs-ui-windows",
	        "1b72vx0",
	        [
	            256
	        ]
	    ],
	    [
	        "oojs-ui.styles.icons",
	        "0ta93u6"
	    ],
	    [
	        "oojs-ui.styles.indicators",
	        "1cot7n6"
	    ],
	    [
	        "oojs-ui.styles.textures",
	        "0g2gxjq"
	    ],
	    [
	        "oojs-ui.styles.icons-accessibility",
	        "0lskeeo"
	    ],
	    [
	        "oojs-ui.styles.icons-alerts",
	        "187n589"
	    ],
	    [
	        "oojs-ui.styles.icons-content",
	        "1psulwp"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-advanced",
	        "1flssey"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-core",
	        "1oycs8m"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-list",
	        "0eoj1rz"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-styling",
	        "0dgozzu"
	    ],
	    [
	        "oojs-ui.styles.icons-interactions",
	        "1ie4c1q"
	    ],
	    [
	        "oojs-ui.styles.icons-layout",
	        "0kcqmn6"
	    ],
	    [
	        "oojs-ui.styles.icons-location",
	        "0qejftq"
	    ],
	    [
	        "oojs-ui.styles.icons-media",
	        "1hb4o6l"
	    ],
	    [
	        "oojs-ui.styles.icons-moderation",
	        "0konovf"
	    ],
	    [
	        "oojs-ui.styles.icons-movement",
	        "0q51gaq"
	    ],
	    [
	        "oojs-ui.styles.icons-user",
	        "1ikh3ag"
	    ],
	    [
	        "oojs-ui.styles.icons-wikimedia",
	        "1gkubqq"
	    ],
	    [
	        "skins.vector.styles",
	        "15on21y"
	    ],
	    [
	        "skins.vector.styles.responsive",
	        "0mxg9d7"
	    ],
	    [
	        "skins.vector.js",
	        "052shly",
	        [
	            53,
	            56
	        ]
	    ],
	    [
	        "ext.tabs",
	        "12wdrkg"
	    ],
	    [
	        "ext.pageforms.main",
	        "11k5tu8",
	        [
	            290,
	            303,
	            289,
	            308,
	            62,
	            101
	        ]
	    ],
	    [
	        "ext.pageforms.browser",
	        "1k0hgas"
	    ],
	    [
	        "ext.pageforms.fancybox.jquery1",
	        "1p1rkqh",
	        [
	            284
	        ]
	    ],
	    [
	        "ext.pageforms.fancybox.jquery3",
	        "047h0sc",
	        [
	            284
	        ]
	    ],
	    [
	        "ext.pageforms.fancytree.dep",
	        "0bjakjb"
	    ],
	    [
	        "ext.pageforms.fancytree",
	        "1fiwt31",
	        [
	            287,
	            70,
	            79
	        ]
	    ],
	    [
	        "ext.pageforms.sortable",
	        "04xwujf"
	    ],
	    [
	        "ext.pageforms.autogrow",
	        "17qlhpp"
	    ],
	    [
	        "ext.pageforms.popupformedit",
	        "168jp4t",
	        [
	            284
	        ]
	    ],
	    [
	        "ext.pageforms.autoedit",
	        "0jtlxdr"
	    ],
	    [
	        "ext.pageforms.submit",
	        "1j1jbea"
	    ],
	    [
	        "ext.pageforms.collapsible",
	        "0h6aqiu"
	    ],
	    [
	        "ext.pageforms.imagepreview",
	        "015bhja"
	    ],
	    [
	        "ext.pageforms.checkboxes",
	        "18yqjk1"
	    ],
	    [
	        "ext.pageforms.datepicker",
	        "08fofed",
	        [
	            283,
	            64
	        ]
	    ],
	    [
	        "ext.pageforms.timepicker",
	        "0zno01o"
	    ],
	    [
	        "ext.pageforms.datetimepicker",
	        "1rioryh",
	        [
	            297,
	            298
	        ]
	    ],
	    [
	        "ext.pageforms.regexp",
	        "174pyfb",
	        [
	            283
	        ]
	    ],
	    [
	        "ext.pageforms.rating",
	        "07ysc1m"
	    ],
	    [
	        "ext.pageforms.simpleupload",
	        "1pbsyn5"
	    ],
	    [
	        "ext.pageforms.select2",
	        "0qp4f7v",
	        [
	            309,
	            75,
	            180
	        ]
	    ],
	    [
	        "ext.pageforms.fullcalendar.jquery1",
	        "178g9u2",
	        [
	            288,
	            303,
	            95
	        ]
	    ],
	    [
	        "ext.pageforms.fullcalendar.jquery3",
	        "1cb001l",
	        [
	            288,
	            303,
	            95
	        ]
	    ],
	    [
	        "ext.pageforms.jsgrid",
	        "0egc82o",
	        [
	            303,
	            181
	        ]
	    ],
	    [
	        "ext.pageforms.balloon",
	        "0675na9"
	    ],
	    [
	        "ext.pageforms.wikieditor",
	        "0yfznuz"
	    ],
	    [
	        "ext.pageforms",
	        "1pc0wl9"
	    ],
	    [
	        "ext.pageforms.PF_CreateProperty",
	        "13p9sb8"
	    ],
	    [
	        "ext.pageforms.PF_PageSchemas",
	        "00ga1av"
	    ],
	    [
	        "ext.pageforms.PF_CreateTemplate",
	        "0tb8erv"
	    ],
	    [
	        "ext.pageforms.PF_CreateClass",
	        "0ciqmrx"
	    ],
	    [
	        "ext.pageforms.PF_CreateForm",
	        "1akoy3t"
	    ],
	    [
	        "ext.categoryTree",
	        "1wwhjjc",
	        [
	            101
	        ]
	    ],
	    [
	        "ext.categoryTree.css",
	        "0mhkoll"
	    ],
	    [
	        "onoi.qtip.core",
	        "1m5bbao"
	    ],
	    [
	        "onoi.qtip.extended",
	        "0jpg0yd"
	    ],
	    [
	        "onoi.qtip",
	        "0b214ac",
	        [
	            318
	        ]
	    ],
	    [
	        "onoi.md5",
	        "15iu0p8"
	    ],
	    [
	        "onoi.blockUI",
	        "029hw49"
	    ],
	    [
	        "onoi.rangeslider",
	        "0ux4iml"
	    ],
	    [
	        "onoi.localForage",
	        "0p06d1l"
	    ],
	    [
	        "onoi.blobstore",
	        "17mr10d",
	        [
	            323
	        ]
	    ],
	    [
	        "onoi.util",
	        "1l9x4ht",
	        [
	            320
	        ]
	    ],
	    [
	        "onoi.async",
	        "1sl29eq"
	    ],
	    [
	        "onoi.jstorage",
	        "0mc9b4f"
	    ],
	    [
	        "onoi.clipboard",
	        "143fg7b"
	    ],
	    [
	        "onoi.bootstrap.tab.styles",
	        "14buvg5"
	    ],
	    [
	        "onoi.bootstrap.tab",
	        "04tnmmm"
	    ],
	    [
	        "onoi.highlight",
	        "1hlxwq3"
	    ],
	    [
	        "onoi.dataTables.styles",
	        "186bakp"
	    ],
	    [
	        "onoi.dataTables.searchHighlight",
	        "1g4g4tl",
	        [
	            331
	        ]
	    ],
	    [
	        "onoi.dataTables.responsive",
	        "15c0w4c",
	        [
	            335
	        ]
	    ],
	    [
	        "onoi.dataTables",
	        "07o3zy2",
	        [
	            333
	        ]
	    ],
	    [
	        "ext.jquery.easing",
	        "1lpii4q"
	    ],
	    [
	        "ext.jquery.fancybox",
	        "0eiy6qq",
	        [
	            336,
	            343
	        ]
	    ],
	    [
	        "ext.jquery.multiselect",
	        "1mukfh6",
	        [
	            59,
	            79
	        ]
	    ],
	    [
	        "ext.jquery.multiselect.filter",
	        "0pib8fv",
	        [
	            338
	        ]
	    ],
	    [
	        "ext.jquery.blockUI",
	        "1kg0b27"
	    ],
	    [
	        "ext.jquery.jqgrid",
	        "0d5hz8o",
	        [
	            343,
	            59
	        ]
	    ],
	    [
	        "ext.jquery.flot",
	        "0b22opp"
	    ],
	    [
	        "ext.jquery.migration.browser",
	        "017i8uz"
	    ],
	    [
	        "ext.srf",
	        "1eprwsp",
	        [
	            448
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.api",
	        "07ypjuj",
	        [
	            344
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.util",
	        "1npg45r",
	        [
	            340,
	            344
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.widgets",
	        "0bt9h05",
	        [
	            338,
	            344,
	            63,
	            74
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.util.grid",
	        "1yh4rax",
	        [
	            341,
	            346,
	            77
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.jquery.sparkline",
	        "0w3hpe9",
	        [
	            343
	        ]
	    ],
	    [
	        "ext.srf.sparkline",
	        "0kvhrvz",
	        [
	            349,
	            346
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.dygraphs.combined",
	        "12otina"
	    ],
	    [
	        "ext.srf.dygraphs",
	        "1srz636",
	        [
	            351,
	            453,
	            346,
	            20
	        ]
	    ],
	    [
	        "ext.jquery.listnav",
	        "1kymtwm"
	    ],
	    [
	        "ext.jquery.listmenu",
	        "0j3f6io"
	    ],
	    [
	        "ext.jquery.pajinate",
	        "0dow2nt"
	    ],
	    [
	        "ext.srf.listwidget",
	        "0qrlbyl",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.srf.listwidget.alphabet",
	        "0b214ac",
	        [
	            353,
	            356
	        ]
	    ],
	    [
	        "ext.srf.listwidget.menu",
	        "0b214ac",
	        [
	            354,
	            356
	        ]
	    ],
	    [
	        "ext.srf.listwidget.pagination",
	        "0b214ac",
	        [
	            355,
	            356
	        ]
	    ],
	    [
	        "ext.jquery.dynamiccarousel",
	        "05gq9gj",
	        [
	            343
	        ]
	    ],
	    [
	        "ext.srf.pagewidget.carousel",
	        "1ue53yn",
	        [
	            360,
	            346
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.core",
	        "08f6tai",
	        [
	            343
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.excanvas",
	        "0rrgnah"
	    ],
	    [
	        "ext.jquery.jqplot.json",
	        "0l4xbgn"
	    ],
	    [
	        "ext.jquery.jqplot.cursor",
	        "0njdqgz"
	    ],
	    [
	        "ext.jquery.jqplot.logaxisrenderer",
	        "1x7b8tx"
	    ],
	    [
	        "ext.jquery.jqplot.mekko",
	        "07zdwad"
	    ],
	    [
	        "ext.jquery.jqplot.bar",
	        "1xo144z",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.pie",
	        "1qwvh51",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.bubble",
	        "0drzpkx",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.donut",
	        "0g9hzrl",
	        [
	            369
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.pointlabels",
	        "0uik9de",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.highlighter",
	        "0rxcg9l",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.enhancedlegend",
	        "014hj98",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.trendline",
	        "1eyp69q"
	    ],
	    [
	        "ext.srf.jqplot.themes",
	        "1nigdjd",
	        [
	            27
	        ]
	    ],
	    [
	        "ext.srf.jqplot.cursor",
	        "0b214ac",
	        [
	            365,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.enhancedlegend",
	        "0b214ac",
	        [
	            374,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.pointlabels",
	        "0b214ac",
	        [
	            372,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.highlighter",
	        "0b214ac",
	        [
	            373,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.trendline",
	        "0b214ac",
	        [
	            375,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.chart",
	        "0mbu56m",
	        [
	            362,
	            376,
	            346,
	            20
	        ]
	    ],
	    [
	        "ext.srf.jqplot.bar",
	        "036d2k9",
	        [
	            368,
	            382
	        ]
	    ],
	    [
	        "ext.srf.jqplot.pie",
	        "0m6gpln",
	        [
	            369,
	            382
	        ]
	    ],
	    [
	        "ext.srf.jqplot.bubble",
	        "0wjnz8g",
	        [
	            370,
	            382
	        ]
	    ],
	    [
	        "ext.srf.jqplot.donut",
	        "0m6gpln",
	        [
	            371,
	            382
	        ]
	    ],
	    [
	        "ext.smile.timeline.core",
	        "0xmxqnl"
	    ],
	    [
	        "ext.smile.timeline",
	        "0jio17t"
	    ],
	    [
	        "ext.srf.timeline",
	        "0j3ayoc",
	        [
	            388,
	            232
	        ]
	    ],
	    [
	        "ext.d3.core",
	        "1sioody"
	    ],
	    [
	        "ext.srf.d3.common",
	        "0cwodu3",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.d3.wordcloud",
	        "00mek1o",
	        [
	            390,
	            391
	        ]
	    ],
	    [
	        "ext.srf.d3.chart.treemap",
	        "1s4uo3a",
	        [
	            390,
	            391
	        ]
	    ],
	    [
	        "ext.srf.d3.chart.bubble",
	        "0ermrlj",
	        [
	            390,
	            391
	        ]
	    ],
	    [
	        "ext.srf.jquery.progressbar",
	        "06p63z2"
	    ],
	    [
	        "ext.srf.jit",
	        "0er3r6j"
	    ],
	    [
	        "ext.srf.jitgraph",
	        "08jplqz",
	        [
	            396,
	            395,
	            232
	        ]
	    ],
	    [
	        "ext.jquery.jcarousel",
	        "0cwt8x9",
	        [
	            343
	        ]
	    ],
	    [
	        "ext.jquery.responsiveslides",
	        "0ubx1v0"
	    ],
	    [
	        "ext.srf.formats.gallery",
	        "1qb8fwt",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.srf.gallery.carousel",
	        "1ncuu2d",
	        [
	            398,
	            400
	        ]
	    ],
	    [
	        "ext.srf.gallery.slideshow",
	        "152iu9x",
	        [
	            399,
	            400
	        ]
	    ],
	    [
	        "ext.srf.gallery.overlay",
	        "15ba26z",
	        [
	            337,
	            400
	        ]
	    ],
	    [
	        "ext.srf.gallery.redirect",
	        "0jw3xjb",
	        [
	            400
	        ]
	    ],
	    [
	        "ext.jquery.fullcalendar",
	        "1j5kocr"
	    ],
	    [
	        "ext.jquery.gcal",
	        "0o9pahf"
	    ],
	    [
	        "ext.srf.widgets.eventcalendar",
	        "0tdsjya",
	        [
	            453,
	            345,
	            346,
	            64,
	            74
	        ]
	    ],
	    [
	        "ext.srf.hooks.eventcalendar",
	        "1nmfm3j",
	        [
	            344
	        ]
	    ],
	    [
	        "ext.srf.eventcalendar",
	        "09wbcyi",
	        [
	            405,
	            408,
	            407
	        ]
	    ],
	    [
	        "ext.srf.filtered",
	        "0yxoc9c",
	        [
	            344
	        ]
	    ],
	    [
	        "ext.srf.filtered.calendar-view.messages",
	        "0f5tfhh"
	    ],
	    [
	        "ext.srf.filtered.calendar-view",
	        "12l5qui",
	        [
	            405,
	            411
	        ]
	    ],
	    [
	        "ext.srf.filtered.map-view.leaflet",
	        "0qatm53"
	    ],
	    [
	        "ext.srf.filtered.map-view",
	        "0ghzic0"
	    ],
	    [
	        "ext.srf.filtered.value-filter",
	        "09lvdnx"
	    ],
	    [
	        "ext.srf.filtered.value-filter.select",
	        "1c5n0jp"
	    ],
	    [
	        "ext.srf.filtered.slider",
	        "1iyp85a"
	    ],
	    [
	        "ext.srf.filtered.distance-filter",
	        "126v31p",
	        [
	            417
	        ]
	    ],
	    [
	        "ext.srf.filtered.number-filter",
	        "0z0u5qz",
	        [
	            417
	        ]
	    ],
	    [
	        "ext.srf.slideshow",
	        "13g68r1",
	        [
	            153
	        ]
	    ],
	    [
	        "ext.jquery.tagcanvas",
	        "0ut5bo5"
	    ],
	    [
	        "ext.srf.formats.tagcloud",
	        "0m5ioh8",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.srf.flot.core",
	        "10dq49o"
	    ],
	    [
	        "ext.srf.timeseries.flot",
	        "0vxlhvy",
	        [
	            342,
	            423,
	            346,
	            20
	        ]
	    ],
	    [
	        "ext.jquery.jplayer",
	        "17mz4ec"
	    ],
	    [
	        "ext.jquery.jplayer.skin.blue.monday",
	        "0c73lki"
	    ],
	    [
	        "ext.jquery.jplayer.skin.morning.light",
	        "14qgayr"
	    ],
	    [
	        "ext.jquery.jplayer.playlist",
	        "1oukaci",
	        [
	            425
	        ]
	    ],
	    [
	        "ext.jquery.jplayer.inspector",
	        "0q6wqb8",
	        [
	            425
	        ]
	    ],
	    [
	        "ext.srf.template.jplayer",
	        "129v1fa",
	        [
	            344
	        ]
	    ],
	    [
	        "ext.srf.formats.media",
	        "0i5zw9t",
	        [
	            428,
	            430
	        ],
	        "ext.srf"
	    ],
	    [
	        "jquery.dataTables",
	        "1ftsqba"
	    ],
	    [
	        "jquery.dataTables.extras",
	        "0jmet9t"
	    ],
	    [
	        "ext.srf.datatables",
	        "1o7w5ft",
	        [
	            345,
	            346,
	            347,
	            432,
	            433
	        ]
	    ],
	    [
	        "ext.srf.datatables.bootstrap",
	        "0xexh7y",
	        [
	            434
	        ]
	    ],
	    [
	        "ext.srf.datatables.basic",
	        "1fqhqez",
	        [
	            434
	        ]
	    ],
	    [
	        "MassEditRegex",
	        "0j9x4cr",
	        [
	            65,
	            180
	        ],
	        "MassEditRegex"
	    ],
	    [
	        "ext.smw",
	        "1n06wzt",
	        [
	            441
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.style",
	        "0hrxpz3",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.special.style",
	        "1vwf6q7",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.async",
	        "1kf1zqt",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.jStorage",
	        "0rqfr57",
	        [
	            94
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.md5",
	        "1rksce9",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.dataItem",
	        "0l40smg",
	        [
	            438,
	            141,
	            150
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.dataValue",
	        "1ocr1rr",
	        [
	            444
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.data",
	        "1c0m7xc",
	        [
	            445
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.query",
	        "0ypvmka",
	        [
	            438,
	            153
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.api",
	        "18auegd",
	        [
	            442,
	            443,
	            446,
	            447
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.autocomplete",
	        "176unvu",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.qtip.styles",
	        "1d0v5kc",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.qtip",
	        "1l3mhdj",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.tooltip.styles",
	        "12v3dph",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.tooltip",
	        "02wchnh",
	        [
	            451,
	            438,
	            452
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.tooltips",
	        "0b214ac",
	        [
	            439,
	            453
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.autocomplete",
	        "0p33s78",
	        [
	            62
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.purge",
	        "1typjra",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.ask",
	        "1lcocbt",
	        [
	            439,
	            453
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.browse.styles",
	        "1vnhr0n",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.browse",
	        "12dqd5n",
	        [
	            439,
	            101
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.browse.page.autocomplete",
	        "0b214ac",
	        [
	            455,
	            459
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.admin",
	        "1lp4zlk",
	        [
	            101
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.property",
	        "1r1j0z7",
	        [
	            449,
	            153
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.pageforms.maps",
	        "09547pi"
	    ]
	] );;

		mw.config.set( {
	    "wgLoadScript": "/wiki/load.php",
	    "debug": true,
	    "skin": "vector",
	    "stylepath": "/wiki/skins",
	    "wgUrlProtocols": "bitcoin\\:|ftp\\:\\/\\/|ftps\\:\\/\\/|geo\\:|git\\:\\/\\/|gopher\\:\\/\\/|http\\:\\/\\/|https\\:\\/\\/|irc\\:\\/\\/|ircs\\:\\/\\/|magnet\\:|mailto\\:|mms\\:\\/\\/|news\\:|nntp\\:\\/\\/|redis\\:\\/\\/|sftp\\:\\/\\/|sip\\:|sips\\:|sms\\:|ssh\\:\\/\\/|svn\\:\\/\\/|tel\\:|telnet\\:\\/\\/|urn\\:|worldwind\\:\\/\\/|xmpp\\:|\\/\\/",
	    "wgArticlePath": "/wiki/$1",
	    "wgScriptPath": "/wiki",
	    "wgScriptExtension": ".php",
	    "wgScript": "/wiki/index.php",
	    "wgSearchType": null,
	    "wgVariantArticlePath": false,
	    "wgActionPaths": {},
	    "wgServer": "//wiki.wizard101central.com",
	    "wgServerName": "wiki.wizard101central.com",
	    "wgUserLanguage": "en",
	    "wgContentLanguage": "en",
	    "wgTranslateNumerals": true,
	    "wgVersion": "1.28.3",
	    "wgEnableAPI": true,
	    "wgEnableWriteAPI": true,
	    "wgMainPageTitle": "Wizard101 Wiki",
	    "wgFormattedNamespaces": {
	        "-2": "Media",
	        "-1": "Special",
	        "0": "",
	        "1": "Talk",
	        "2": "User",
	        "3": "User talk",
	        "4": "Wizard101 Wiki",
	        "5": "Wizard101 Wiki talk",
	        "6": "File",
	        "7": "File talk",
	        "8": "MediaWiki",
	        "9": "MediaWiki talk",
	        "10": "Template",
	        "11": "Template talk",
	        "12": "Help",
	        "13": "Help talk",
	        "14": "Category",
	        "15": "Category talk",
	        "100": "Creature",
	        "102": "Spell",
	        "104": "Pet",
	        "106": "Location",
	        "108": "NPC",
	        "110": "Quest",
	        "112": "Item",
	        "114": "Minion",
	        "116": "TreasureCard",
	        "118": "ItemCard",
	        "120": "Reagent",
	        "122": "Snack",
	        "124": "PetAbility",
	        "128": "Mount",
	        "130": "House",
	        "132": "Basic",
	        "134": "Polymorph",
	        "136": "Contest",
	        "138": "Fish",
	        "140": "LockedChest",
	        "142": "Jewel",
	        "144": "Recipe",
	        "146": "BeastmoonForm",
	        "148": "Set",
	        "152": "Property",
	        "153": "Property talk",
	        "156": "Form",
	        "157": "Form talk",
	        "158": "Concept",
	        "159": "Concept talk"
	    },
	    "wgNamespaceIds": {
	        "media": -2,
	        "special": -1,
	        "": 0,
	        "talk": 1,
	        "user": 2,
	        "user_talk": 3,
	        "wizard101_wiki": 4,
	        "wizard101_wiki_talk": 5,
	        "file": 6,
	        "file_talk": 7,
	        "mediawiki": 8,
	        "mediawiki_talk": 9,
	        "template": 10,
	        "template_talk": 11,
	        "help": 12,
	        "help_talk": 13,
	        "category": 14,
	        "category_talk": 15,
	        "creature": 100,
	        "spell": 102,
	        "pet": 104,
	        "location": 106,
	        "npc": 108,
	        "quest": 110,
	        "item": 112,
	        "minion": 114,
	        "treasurecard": 116,
	        "itemcard": 118,
	        "reagent": 120,
	        "snack": 122,
	        "petability": 124,
	        "mount": 128,
	        "house": 130,
	        "basic": 132,
	        "polymorph": 134,
	        "contest": 136,
	        "fish": 138,
	        "lockedchest": 140,
	        "jewel": 142,
	        "recipe": 144,
	        "beastmoonform": 146,
	        "set": 148,
	        "property": 152,
	        "property_talk": 153,
	        "form": 156,
	        "form_talk": 157,
	        "concept": 158,
	        "concept_talk": 159,
	        "image": 6,
	        "image_talk": 7,
	        "project": 4,
	        "project_talk": 5
	    },
	    "wgContentNamespaces": [
	        0,
	        100,
	        102,
	        104,
	        106,
	        108,
	        110,
	        112,
	        114,
	        116,
	        118,
	        120,
	        122,
	        124,
	        128,
	        130,
	        132,
	        134,
	        136,
	        138,
	        140,
	        142,
	        144,
	        146,
	        148
	    ],
	    "wgSiteName": "Wizard101 Wiki",
	    "wgDBname": "wikidb3",
	    "wgExtraSignatureNamespaces": [],
	    "wgAvailableSkins": {
	        "vector": "Vector",
	        "fallback": "Fallback",
	        "apioutput": "ApiOutput"
	    },
	    "wgExtensionAssetsPath": "/wiki/extensions",
	    "wgCookiePrefix": "wikidb3_mw_",
	    "wgCookieDomain": "",
	    "wgCookiePath": "/",
	    "wgCookieExpiration": 15552000,
	    "wgResourceLoaderMaxQueryLength": 2000,
	    "wgCaseSensitiveNamespaces": [],
	    "wgLegalTitleChars": " %!\"$&'()*,\\-./0-9:;=?@A-Z\\\\\\^_`a-z~+\\u0080-\\uFFFF",
	    "wgIllegalFileChars": ":/\\\\",
	    "wgResourceLoaderStorageVersion": 1,
	    "wgResourceLoaderStorageEnabled": true,
	    "wgResourceLoaderLegacyModules": [],
	    "wgForeignUploadTargets": [
	        "local"
	    ],
	    "wgEnableUploads": true,
	    "srf-config": {
	        "version": "2.5.6",
	        "settings": {
	            "wgThumbLimits": [
	                120,
	                150,
	                180,
	                200,
	                250,
	                300
	            ],
	            "srfgScriptPath": "/wiki/extensions/SemanticResultFormats"
	        }
	    },
	    "smw-config": {
	        "version": "2.5.8",
	        "settings": {
	            "smwgQMaxLimit": 10000,
	            "smwgQMaxInlineLimit": 500,
	            "namespace": {
	                "Property": 152,
	                "Property_talk": 153,
	                "Concept": 158,
	                "Concept_talk": 159,
	                "Basic": 132,
	                "Contest": 136,
	                "Creature": 100,
	                "Fish": 138,
	                "House": 130,
	                "Item": 112,
	                "ItemCard": 118,
	                "Jewel": 142,
	                "Location": 106,
	                "LockedChest": 140,
	                "Minion": 114,
	                "Mount": 128,
	                "NPC": 108,
	                "Pet": 104,
	                "PetAbility": 124,
	                "Polymorph": 134,
	                "Quest": 110,
	                "Reagent": 120,
	                "Recipe": 144,
	                "Snack": 122,
	                "Spell": 102,
	                "TreasureCard": 116,
	                "Category": 14,
	                "Category_talk": 15,
	                "Help": 12,
	                "Help_talk": 13,
	                "": 0,
	                "MediaWiki": 8,
	                "MediaWiki_talk": 9,
	                "Talk": 1,
	                "Template": 10,
	                "Template_talk": 11,
	                "User": 2,
	                "User_talk": 3,
	                "File": 6,
	                "File_talk": 7,
	                "Project": 4,
	                "Project_talk": 5,
	                "0": 155,
	                "BeastmoonForm": 146,
	                "Set": 148
	            }
	        },
	        "formats": {
	            "table": "table",
	            "list": "list",
	            "ol": "ol",
	            "ul": "ul",
	            "broadtable": "broadtable",
	            "category": "category",
	            "embedded": "embedded",
	            "template": "template",
	            "count": "count",
	            "debug": "debug",
	            "feed": "feed",
	            "csv": "csv",
	            "dsv": "dsv",
	            "json": "json",
	            "rdf": "rdf",
	            "icalendar": "icalendar",
	            "vcard": "vcard",
	            "bibtex": "bibtex",
	            "calendar": "calendar",
	            "eventcalendar": "eventcalendar",
	            "eventline": "eventline",
	            "timeline": "timeline",
	            "outline": "outline",
	            "gallery": "gallery",
	            "jqplotchart": "jqplotchart",
	            "jqplotseries": "jqplotseries",
	            "sum": "sum",
	            "average": "average",
	            "min": "min",
	            "max": "max",
	            "median": "median",
	            "product": "product",
	            "tagcloud": "tagcloud",
	            "valuerank": "valuerank",
	            "array": "array",
	            "tree": "tree",
	            "ultree": "ultree",
	            "oltree": "oltree",
	            "d3chart": "d3chart",
	            "latest": "latest",
	            "earliest": "earliest",
	            "filtered": "filtered",
	            "slideshow": "slideshow",
	            "timeseries": "timeseries",
	            "sparkline": "sparkline",
	            "listwidget": "listwidget",
	            "pagewidget": "pagewidget",
	            "dygraphs": "dygraphs",
	            "media": "media",
	            "datatables": "datatables"
	        }
	    }
	} );

		// Must be after mw.config.set because these callbacks may use mw.loader which
		// needs to have values 'skin', 'debug' etc. from mw.config.
		var RLQ = window.RLQ || [];
		while ( RLQ.length ) {
			RLQ.shift()();
		}
		window.RLQ = {
			push: function ( fn ) {
				fn();
			}
		};

		// Clear and disable the other queue
		window.NORLQ = {
			// No-op
			push: function () {}
		};
	}

	script = document.createElement( 'script' );
	script.src = "/wiki/load.php?debug=true&lang=en&modules=jquery%2Cmediawiki&only=scripts&skin=vector&version=0dxa7bn";
	script.onload = script.onreadystatechange = function () {
		if ( !script.readyState || /loaded|complete/.test( script.readyState ) ) {
			// Clean up
			script.onload = script.onreadystatechange = null;
			script = null;
			// Callback
			startUp();
		}
	};
	document.getElementsByTagName( 'head' )[ 0 ].appendChild( script );
}() );
