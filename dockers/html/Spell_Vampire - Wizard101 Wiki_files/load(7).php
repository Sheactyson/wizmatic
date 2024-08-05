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
	        "1d6234h",
	        [
	            1
	        ]
	    ],
	    [
	        "site.styles",
	        "00icbf7",
	        [],
	        "site"
	    ],
	    [
	        "noscript",
	        "074icgv",
	        [],
	        "noscript"
	    ],
	    [
	        "filepage",
	        "1iz549g"
	    ],
	    [
	        "user.groups",
	        "06sr3r6",
	        [
	            5
	        ]
	    ],
	    [
	        "user",
	        "088v246",
	        [
	            6
	        ],
	        "user"
	    ],
	    [
	        "user.styles",
	        "0symtq8",
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
	        "010hzhu",
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
	        "1aw5ou1"
	    ],
	    [
	        "mediawiki.skinning.content",
	        "1vj1c3w"
	    ],
	    [
	        "mediawiki.skinning.interface",
	        "1u2ljgl"
	    ],
	    [
	        "mediawiki.skinning.content.parsoid",
	        "0un29tf"
	    ],
	    [
	        "mediawiki.skinning.content.externallinks",
	        "1c8rqnz"
	    ],
	    [
	        "jquery.accessKeyLabel",
	        "1f6y9p7",
	        [
	            27,
	            136
	        ]
	    ],
	    [
	        "jquery.appear",
	        "1eo35oh"
	    ],
	    [
	        "jquery.arrowSteps",
	        "07bzf3w"
	    ],
	    [
	        "jquery.async",
	        "1phjum5"
	    ],
	    [
	        "jquery.autoEllipsis",
	        "12yqjv7",
	        [
	            39
	        ]
	    ],
	    [
	        "jquery.badge",
	        "009n6t0",
	        [
	            176
	        ]
	    ],
	    [
	        "jquery.byteLength",
	        "0ojzs6k"
	    ],
	    [
	        "jquery.byteLimit",
	        "171vnsj",
	        [
	            23
	        ]
	    ],
	    [
	        "jquery.checkboxShiftClick",
	        "0bbkye7"
	    ],
	    [
	        "jquery.chosen",
	        "1kzt61b"
	    ],
	    [
	        "jquery.client",
	        "0vlj9c6"
	    ],
	    [
	        "jquery.color",
	        "1kpjunb",
	        [
	            29
	        ]
	    ],
	    [
	        "jquery.colorUtil",
	        "1uxj38v"
	    ],
	    [
	        "jquery.confirmable",
	        "0wluol4",
	        [
	            180
	        ]
	    ],
	    [
	        "jquery.cookie",
	        "0dyex0e"
	    ],
	    [
	        "jquery.expandableField",
	        "1l066i7"
	    ],
	    [
	        "jquery.farbtastic",
	        "0xj3zfm",
	        [
	            29
	        ]
	    ],
	    [
	        "jquery.footHovzer",
	        "1786im6"
	    ],
	    [
	        "jquery.form",
	        "0k5cui3"
	    ],
	    [
	        "jquery.fullscreen",
	        "1gusmwb"
	    ],
	    [
	        "jquery.getAttrs",
	        "12a2exw"
	    ],
	    [
	        "jquery.hidpi",
	        "0fukdox"
	    ],
	    [
	        "jquery.highlightText",
	        "1sphujt",
	        [
	            251,
	            136
	        ]
	    ],
	    [
	        "jquery.hoverIntent",
	        "0kjkk7x"
	    ],
	    [
	        "jquery.i18n",
	        "1pjt498",
	        [
	            178
	        ]
	    ],
	    [
	        "jquery.localize",
	        "0a2bhuz"
	    ],
	    [
	        "jquery.makeCollapsible",
	        "098jbma"
	    ],
	    [
	        "jquery.mockjax",
	        "00xq67q"
	    ],
	    [
	        "jquery.mw-jump",
	        "1d750yc"
	    ],
	    [
	        "jquery.mwExtension",
	        "1jc3ofo"
	    ],
	    [
	        "jquery.placeholder",
	        "1uuyj2n"
	    ],
	    [
	        "jquery.qunit",
	        "148n3em"
	    ],
	    [
	        "jquery.qunit.completenessTest",
	        "18m4qiq",
	        [
	            48
	        ]
	    ],
	    [
	        "jquery.spinner",
	        "1mzt9w5"
	    ],
	    [
	        "jquery.jStorage",
	        "1k5a8hf",
	        [
	            94
	        ]
	    ],
	    [
	        "jquery.suggestions",
	        "0fbz8m0",
	        [
	            39
	        ]
	    ],
	    [
	        "jquery.tabIndex",
	        "15s0nax"
	    ],
	    [
	        "jquery.tablesorter",
	        "18w0bxd",
	        [
	            251,
	            136,
	            181
	        ]
	    ],
	    [
	        "jquery.textSelection",
	        "1yhjzgy",
	        [
	            27
	        ]
	    ],
	    [
	        "jquery.throttle-debounce",
	        "19659nm"
	    ],
	    [
	        "jquery.xmldom",
	        "1vsnxml"
	    ],
	    [
	        "jquery.tipsy",
	        "0jlxak8"
	    ],
	    [
	        "jquery.ui.core",
	        "127ywnk",
	        [
	            60
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.core.styles",
	        "1l8q2eg",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.accordion",
	        "06crpb6",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.autocomplete",
	        "1nn36gb",
	        [
	            68
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.button",
	        "1yf34fi",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.datepicker",
	        "1rnqwc9",
	        [
	            59
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.dialog",
	        "0sk7b8d",
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
	        "12ke4y0",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.droppable",
	        "15470ix",
	        [
	            66
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.menu",
	        "022nhko",
	        [
	            59,
	            70,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.mouse",
	        "0nxmqa8",
	        [
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.position",
	        "0vsgmw9",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.progressbar",
	        "1fexsvi",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.resizable",
	        "08c3nfv",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.selectable",
	        "0ucx72w",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.slider",
	        "023n678",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.sortable",
	        "1ntpgfk",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.spinner",
	        "11c03rg",
	        [
	            63
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.tabs",
	        "119exxj",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.tooltip",
	        "15vbimv",
	        [
	            59,
	            70,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.widget",
	        "1xrstdz",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.core",
	        "0u1lxhn",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.blind",
	        "1rnhovm",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.bounce",
	        "1ogoa0e",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.clip",
	        "06324zz",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.drop",
	        "1228qqf",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.explode",
	        "114ms5k",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.fade",
	        "0ziz1qu",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.fold",
	        "13nifx6",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.highlight",
	        "0eq4p2s",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.pulsate",
	        "0ywn80c",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.scale",
	        "1mq4nd0",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.shake",
	        "0rv5x33",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.slide",
	        "0gn6hsg",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.transfer",
	        "0hiibxi",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "json",
	        "08op9g3",
	        [],
	        null,
	        null,
	        "/*!\n * Skip function for json2.js.\n */\nreturn !!( window.JSON \u0026\u0026 JSON.stringify \u0026\u0026 JSON.parse );\n"
	    ],
	    [
	        "moment",
	        "0xtn479",
	        [
	            176
	        ]
	    ],
	    [
	        "mediawiki.apihelp",
	        "0fogaft"
	    ],
	    [
	        "mediawiki.template",
	        "056htfj"
	    ],
	    [
	        "mediawiki.template.mustache",
	        "11mcwrd",
	        [
	            97
	        ]
	    ],
	    [
	        "mediawiki.template.regexp",
	        "13fuyh5",
	        [
	            97
	        ]
	    ],
	    [
	        "mediawiki.apipretty",
	        "0f0nmtp"
	    ],
	    [
	        "mediawiki.api",
	        "1sfp52y",
	        [
	            153,
	            10
	        ]
	    ],
	    [
	        "mediawiki.api.category",
	        "1uk1blu",
	        [
	            141,
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.edit",
	        "0mv33vw",
	        [
	            141,
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.login",
	        "135nfke",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.options",
	        "11hce5x",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.parse",
	        "1oos8fv",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.upload",
	        "13qdbkv",
	        [
	            251,
	            94,
	            103
	        ]
	    ],
	    [
	        "mediawiki.api.user",
	        "03a28w8",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.watch",
	        "1xhuckl",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.messages",
	        "0oku0kc",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.rollback",
	        "1i8da3a",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.content.json",
	        "01ab967"
	    ],
	    [
	        "mediawiki.confirmCloseWindow",
	        "0ml3fqb"
	    ],
	    [
	        "mediawiki.debug",
	        "1si7l8m",
	        [
	            34
	        ]
	    ],
	    [
	        "mediawiki.diff.styles",
	        "1fz8ghy"
	    ],
	    [
	        "mediawiki.feedback",
	        "0arcj8f",
	        [
	            141,
	            130,
	            260
	        ]
	    ],
	    [
	        "mediawiki.feedlink",
	        "148xtlk"
	    ],
	    [
	        "mediawiki.filewarning",
	        "1b9671b",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.ForeignApi",
	        "0fhrhxc",
	        [
	            120
	        ]
	    ],
	    [
	        "mediawiki.ForeignApi.core",
	        "1sfy85b",
	        [
	            101,
	            252
	        ]
	    ],
	    [
	        "mediawiki.helplink",
	        "15qivly"
	    ],
	    [
	        "mediawiki.hidpi",
	        "0ivgamm",
	        [
	            38
	        ],
	        null,
	        null,
	        "/*!\n * Skip function for mediawiki.hdpi.js.\n */\nreturn 'srcset' in new Image();\n"
	    ],
	    [
	        "mediawiki.hlist",
	        "0xlfx8h"
	    ],
	    [
	        "mediawiki.htmlform",
	        "12ecytb",
	        [
	            24,
	            136
	        ]
	    ],
	    [
	        "mediawiki.htmlform.ooui",
	        "0n82102",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.htmlform.styles",
	        "1alutqy"
	    ],
	    [
	        "mediawiki.htmlform.ooui.styles",
	        "0kn854h"
	    ],
	    [
	        "mediawiki.icon",
	        "01xm904"
	    ],
	    [
	        "mediawiki.inspect",
	        "167cbv7",
	        [
	            23,
	            94,
	            136
	        ]
	    ],
	    [
	        "mediawiki.messagePoster",
	        "1sex7vw",
	        [
	            119
	        ]
	    ],
	    [
	        "mediawiki.messagePoster.wikitext",
	        "0n5er6y",
	        [
	            103,
	            130
	        ]
	    ],
	    [
	        "mediawiki.notification",
	        "1eyo6fg",
	        [
	            189
	        ]
	    ],
	    [
	        "mediawiki.notify",
	        "0cryrh6"
	    ],
	    [
	        "mediawiki.notification.convertmessagebox",
	        "0cucoln",
	        [
	            132
	        ]
	    ],
	    [
	        "mediawiki.notification.convertmessagebox.styles",
	        "06vipgg"
	    ],
	    [
	        "mediawiki.RegExp",
	        "16etdzw"
	    ],
	    [
	        "mediawiki.pager.tablePager",
	        "163vjrs"
	    ],
	    [
	        "mediawiki.searchSuggest",
	        "149kuxe",
	        [
	            37,
	            47,
	            52,
	            101
	        ]
	    ],
	    [
	        "mediawiki.sectionAnchor",
	        "02yrudm"
	    ],
	    [
	        "mediawiki.storage",
	        "1nykxzw"
	    ],
	    [
	        "mediawiki.Title",
	        "10dadz3",
	        [
	            23,
	            153
	        ]
	    ],
	    [
	        "mediawiki.Upload",
	        "0rceku5",
	        [
	            107
	        ]
	    ],
	    [
	        "mediawiki.ForeignUpload",
	        "1yp1pr6",
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
	        "0j8ongd",
	        [
	            144,
	            143
	        ]
	    ],
	    [
	        "mediawiki.Upload.Dialog",
	        "0sgzxwm",
	        [
	            147
	        ]
	    ],
	    [
	        "mediawiki.Upload.BookletLayout",
	        "1fm7ugq",
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
	        "1qq7du0",
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
	        "0b4ssyw",
	        [
	            157
	        ]
	    ],
	    [
	        "mediawiki.Uri",
	        "0cud9qh",
	        [
	            153,
	            99
	        ]
	    ],
	    [
	        "mediawiki.user",
	        "0i2eu1m",
	        [
	            108,
	            157,
	            9
	        ]
	    ],
	    [
	        "mediawiki.userSuggest",
	        "0fh6jop",
	        [
	            52,
	            101
	        ]
	    ],
	    [
	        "mediawiki.util",
	        "0oyw2ji",
	        [
	            17,
	            133
	        ]
	    ],
	    [
	        "mediawiki.viewport",
	        "0nafnrq"
	    ],
	    [
	        "mediawiki.checkboxtoggle",
	        "08tupe7"
	    ],
	    [
	        "mediawiki.checkboxtoggle.styles",
	        "0a4ubkf"
	    ],
	    [
	        "mediawiki.cookie",
	        "0329i7s",
	        [
	            31
	        ]
	    ],
	    [
	        "mediawiki.toolbar",
	        "0kk495p",
	        [
	            55
	        ]
	    ],
	    [
	        "mediawiki.experiments",
	        "031sfn6"
	    ],
	    [
	        "mediawiki.action.edit",
	        "1ya7lke",
	        [
	            24,
	            55,
	            161,
	            101
	        ]
	    ],
	    [
	        "mediawiki.action.edit.styles",
	        "0zzrro1"
	    ],
	    [
	        "mediawiki.action.edit.collapsibleFooter",
	        "1vnshrv",
	        [
	            43,
	            157,
	            128
	        ]
	    ],
	    [
	        "mediawiki.action.edit.preview",
	        "0mkmnp0",
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
	        "1ym44vz"
	    ],
	    [
	        "mediawiki.action.history.styles",
	        "1fahd5r"
	    ],
	    [
	        "mediawiki.action.history.diff",
	        "1fz8ghy"
	    ],
	    [
	        "mediawiki.action.view.dblClickEdit",
	        "1wc9f00",
	        [
	            189,
	            9
	        ]
	    ],
	    [
	        "mediawiki.action.view.metadata",
	        "0zcdnus"
	    ],
	    [
	        "mediawiki.action.view.categoryPage.styles",
	        "0abdcon"
	    ],
	    [
	        "mediawiki.action.view.postEdit",
	        "07y376g",
	        [
	            157,
	            180,
	            97
	        ]
	    ],
	    [
	        "mediawiki.action.view.redirect",
	        "1gfjcrh",
	        [
	            27
	        ]
	    ],
	    [
	        "mediawiki.action.view.redirectPage",
	        "0ff1jvl"
	    ],
	    [
	        "mediawiki.action.view.rightClickEdit",
	        "1qnvd4s"
	    ],
	    [
	        "mediawiki.action.edit.editWarning",
	        "0g7oa7k",
	        [
	            55,
	            113,
	            180
	        ]
	    ],
	    [
	        "mediawiki.action.view.filepage",
	        "1obfhlw"
	    ],
	    [
	        "mediawiki.language",
	        "0pbhx4s",
	        [
	            177,
	            11
	        ]
	    ],
	    [
	        "mediawiki.cldr",
	        "1ongcsz",
	        [
	            178
	        ]
	    ],
	    [
	        "mediawiki.libs.pluralruleparser",
	        "1wry4u1"
	    ],
	    [
	        "mediawiki.language.init",
	        "0xd2ucg"
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
	        "0xyqygv",
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
	        "0z7e2k0"
	    ],
	    [
	        "mediawiki.page.gallery",
	        "0pcu5tf",
	        [
	            56,
	            186
	        ]
	    ],
	    [
	        "mediawiki.page.gallery.styles",
	        "0m69rwh"
	    ],
	    [
	        "mediawiki.page.gallery.slideshow",
	        "1ppe6w7",
	        [
	            141,
	            101,
	            258,
	            274
	        ]
	    ],
	    [
	        "mediawiki.page.ready",
	        "055g96b",
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
	        "1nlh7h6",
	        [
	            153
	        ]
	    ],
	    [
	        "mediawiki.page.patrol.ajax",
	        "18v2bri",
	        [
	            50,
	            141,
	            101,
	            189
	        ]
	    ],
	    [
	        "mediawiki.page.watch.ajax",
	        "1cmtbl2",
	        [
	            109,
	            189
	        ]
	    ],
	    [
	        "mediawiki.page.rollback",
	        "15ja88k",
	        [
	            50,
	            111
	        ]
	    ],
	    [
	        "mediawiki.page.image.pagination",
	        "099m54l",
	        [
	            50,
	            153
	        ]
	    ],
	    [
	        "mediawiki.special",
	        "0i56bqx"
	    ],
	    [
	        "mediawiki.special.apisandbox.styles",
	        "1n0r5tp"
	    ],
	    [
	        "mediawiki.special.apisandbox",
	        "1whgvei",
	        [
	            101,
	            180,
	            244,
	            255
	        ]
	    ],
	    [
	        "mediawiki.special.block",
	        "0qataes",
	        [
	            153
	        ]
	    ],
	    [
	        "mediawiki.special.changeslist",
	        "17tico4"
	    ],
	    [
	        "mediawiki.special.changeslist.legend",
	        "1npicrt"
	    ],
	    [
	        "mediawiki.special.changeslist.legend.js",
	        "0dx053z",
	        [
	            43,
	            157
	        ]
	    ],
	    [
	        "mediawiki.special.changeslist.enhanced",
	        "1iw28zw"
	    ],
	    [
	        "mediawiki.special.changeslist.visitedstatus",
	        "0087fo1"
	    ],
	    [
	        "mediawiki.special.comparepages.styles",
	        "1o3k5o9"
	    ],
	    [
	        "mediawiki.special.edittags",
	        "0eyjxpk",
	        [
	            26
	        ]
	    ],
	    [
	        "mediawiki.special.edittags.styles",
	        "0f2tp0j"
	    ],
	    [
	        "mediawiki.special.import",
	        "1ldzl76"
	    ],
	    [
	        "mediawiki.special.movePage",
	        "0hxmn27",
	        [
	            241
	        ]
	    ],
	    [
	        "mediawiki.special.movePage.styles",
	        "01jktrj"
	    ],
	    [
	        "mediawiki.special.pageLanguage",
	        "1g5c3cr",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.special.pagesWithProp",
	        "0iybjd0"
	    ],
	    [
	        "mediawiki.special.preferences",
	        "1tqfb9c",
	        [
	            113,
	            176,
	            134
	        ]
	    ],
	    [
	        "mediawiki.special.userrights",
	        "0a0lxmv",
	        [
	            134
	        ]
	    ],
	    [
	        "mediawiki.special.preferences.styles",
	        "0sm3iwb"
	    ],
	    [
	        "mediawiki.special.recentchanges",
	        "0oa353z"
	    ],
	    [
	        "mediawiki.special.search",
	        "1xy1sc0",
	        [
	            247
	        ]
	    ],
	    [
	        "mediawiki.special.search.styles",
	        "1f8lvvn"
	    ],
	    [
	        "mediawiki.special.undelete",
	        "14dehca"
	    ],
	    [
	        "mediawiki.special.upload",
	        "1jkd3bq",
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
	        "0hb2mjy"
	    ],
	    [
	        "mediawiki.special.userlogin.common.styles",
	        "0ejhcou"
	    ],
	    [
	        "mediawiki.special.userlogin.signup.styles",
	        "00cqlof"
	    ],
	    [
	        "mediawiki.special.userlogin.login.styles",
	        "1xr37j2"
	    ],
	    [
	        "mediawiki.special.userlogin.signup.js",
	        "1999vj7",
	        [
	            56,
	            101,
	            180
	        ]
	    ],
	    [
	        "mediawiki.special.unwatchedPages",
	        "0mbzvss",
	        [
	            141,
	            109
	        ]
	    ],
	    [
	        "mediawiki.special.watchlist",
	        "0r6fsvm"
	    ],
	    [
	        "mediawiki.special.version",
	        "13l38zc"
	    ],
	    [
	        "mediawiki.legacy.config",
	        "0winqe1"
	    ],
	    [
	        "mediawiki.legacy.commonPrint",
	        "0fi50c9"
	    ],
	    [
	        "mediawiki.legacy.protect",
	        "0aeampd",
	        [
	            24
	        ]
	    ],
	    [
	        "mediawiki.legacy.shared",
	        "177gn2y"
	    ],
	    [
	        "mediawiki.legacy.oldshared",
	        "1spw9t2"
	    ],
	    [
	        "mediawiki.legacy.wikibits",
	        "1lpa55i",
	        [
	            153
	        ]
	    ],
	    [
	        "mediawiki.ui",
	        "0lf0pbx"
	    ],
	    [
	        "mediawiki.ui.checkbox",
	        "0rh6zvs"
	    ],
	    [
	        "mediawiki.ui.radio",
	        "1unlpb8"
	    ],
	    [
	        "mediawiki.ui.anchor",
	        "14jhv6w"
	    ],
	    [
	        "mediawiki.ui.button",
	        "0waijty"
	    ],
	    [
	        "mediawiki.ui.input",
	        "0ajvfpb"
	    ],
	    [
	        "mediawiki.ui.icon",
	        "0urabjo"
	    ],
	    [
	        "mediawiki.ui.text",
	        "0bskyv7"
	    ],
	    [
	        "mediawiki.widgets",
	        "0uy5xm2",
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
	        "0mkymgp"
	    ],
	    [
	        "mediawiki.widgets.DateInputWidget",
	        "19o24av",
	        [
	            95,
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.datetime",
	        "0ch9qdc",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.widgets.CategorySelector",
	        "164vgth",
	        [
	            119,
	            141,
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.UserInputWidget",
	        "0bnp3fz",
	        [
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.SearchInputWidget",
	        "0lbregt",
	        [
	            138,
	            241
	        ]
	    ],
	    [
	        "mediawiki.widgets.SearchInputWidget.styles",
	        "116nz1b"
	    ],
	    [
	        "mediawiki.widgets.StashedFileWidget",
	        "0062pgp",
	        [
	            256
	        ]
	    ],
	    [
	        "es5-shim",
	        "00v3zbh",
	        [],
	        null,
	        null,
	        "/*!\n * Skip function for es5-shim module.\n *\n * Test for strict mode as a proxy for full ES5 function support (but not syntax)\n * Per http://kangax.github.io/compat-table/es5/ this is a reasonable shortcut\n * that still allows this to be as short as possible (there are no browsers we\n * support that have strict mode, but lack other features).\n *\n * Do explicitly test for Function#bind because of PhantomJS (which implements\n * strict mode, but lacks Function#bind).\n *\n * IE9 supports all features except strict mode, so loading es5-shim should be close to\n * a no-op but does increase page payload).\n */\nreturn ( function () {\n\t'use strict';\n\treturn !this \u0026\u0026 !!Function.prototype.bind;\n}() );\n"
	    ],
	    [
	        "dom-level2-shim",
	        "0qprmdn",
	        [],
	        null,
	        null,
	        "/*!\n * Skip function for dom-level2-shim module.\n *\n * Tests for window.Node because that's the only thing that this shim is adding.\n */\nreturn !!window.Node;\n"
	    ],
	    [
	        "oojs",
	        "1t1cq3i",
	        [
	            250,
	            94
	        ]
	    ],
	    [
	        "mediawiki.router",
	        "1reky21",
	        [
	            254
	        ]
	    ],
	    [
	        "oojs-router",
	        "1nv656z",
	        [
	            252
	        ]
	    ],
	    [
	        "oojs-ui",
	        "06sr3r6",
	        [
	            259,
	            258,
	            260
	        ]
	    ],
	    [
	        "oojs-ui-core",
	        "0plk1n5",
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
	        "0c1rww6"
	    ],
	    [
	        "oojs-ui-widgets",
	        "18yrgod",
	        [
	            256
	        ]
	    ],
	    [
	        "oojs-ui-toolbars",
	        "1vsbxn8",
	        [
	            256
	        ]
	    ],
	    [
	        "oojs-ui-windows",
	        "1y7pvda",
	        [
	            256
	        ]
	    ],
	    [
	        "oojs-ui.styles.icons",
	        "0i8t148"
	    ],
	    [
	        "oojs-ui.styles.indicators",
	        "0dcd9pk"
	    ],
	    [
	        "oojs-ui.styles.textures",
	        "117zosc"
	    ],
	    [
	        "oojs-ui.styles.icons-accessibility",
	        "09mqwgi"
	    ],
	    [
	        "oojs-ui.styles.icons-alerts",
	        "0h4itab"
	    ],
	    [
	        "oojs-ui.styles.icons-content",
	        "1nlq7rr"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-advanced",
	        "0ppp2gc"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-core",
	        "1hl0ty4"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-list",
	        "19de8s9"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-styling",
	        "070f0dg"
	    ],
	    [
	        "oojs-ui.styles.icons-interactions",
	        "129nbws"
	    ],
	    [
	        "oojs-ui.styles.icons-layout",
	        "1gw2bp8"
	    ],
	    [
	        "oojs-ui.styles.icons-location",
	        "1pxvt2k"
	    ],
	    [
	        "oojs-ui.styles.icons-media",
	        "1perhfv"
	    ],
	    [
	        "oojs-ui.styles.icons-moderation",
	        "129mf71"
	    ],
	    [
	        "oojs-ui.styles.icons-movement",
	        "0toj8ik"
	    ],
	    [
	        "oojs-ui.styles.icons-user",
	        "0su223y"
	    ],
	    [
	        "oojs-ui.styles.icons-wikimedia",
	        "17k1b4o"
	    ],
	    [
	        "skins.vector.styles",
	        "0eukczc"
	    ],
	    [
	        "skins.vector.styles.responsive",
	        "1uqw37t"
	    ],
	    [
	        "skins.vector.js",
	        "0p6xgjw",
	        [
	            53,
	            56
	        ]
	    ],
	    [
	        "ext.tabs",
	        "1dporvy"
	    ],
	    [
	        "ext.pageforms.main",
	        "09oiss6",
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
	        "1wkc3ya"
	    ],
	    [
	        "ext.pageforms.fancybox.jquery1",
	        "1461tzj",
	        [
	            284
	        ]
	    ],
	    [
	        "ext.pageforms.fancybox.jquery3",
	        "1xe7kxm",
	        [
	            284
	        ]
	    ],
	    [
	        "ext.pageforms.fancytree.dep",
	        "136sbxl"
	    ],
	    [
	        "ext.pageforms.fancytree",
	        "1y82l5j",
	        [
	            287,
	            70,
	            79
	        ]
	    ],
	    [
	        "ext.pageforms.sortable",
	        "0hp7dbh"
	    ],
	    [
	        "ext.pageforms.autogrow",
	        "1ys58lb"
	    ],
	    [
	        "ext.pageforms.popupformedit",
	        "0tg9cxf",
	        [
	            284
	        ]
	    ],
	    [
	        "ext.pageforms.autoedit",
	        "12n3f5p"
	    ],
	    [
	        "ext.pageforms.submit",
	        "043l1hk"
	    ],
	    [
	        "ext.pageforms.collapsible",
	        "12std2w"
	    ],
	    [
	        "ext.pageforms.imagepreview",
	        "0wc9y4g"
	    ],
	    [
	        "ext.pageforms.checkboxes",
	        "0b0c96z"
	    ],
	    [
	        "ext.pageforms.datepicker",
	        "0bc9dzn",
	        [
	            283,
	            64
	        ]
	    ],
	    [
	        "ext.pageforms.timepicker",
	        "0yccx46"
	    ],
	    [
	        "ext.pageforms.datetimepicker",
	        "02cg0sr",
	        [
	            297,
	            298
	        ]
	    ],
	    [
	        "ext.pageforms.regexp",
	        "1eaknxl",
	        [
	            283
	        ]
	    ],
	    [
	        "ext.pageforms.rating",
	        "16m12sw"
	    ],
	    [
	        "ext.pageforms.simpleupload",
	        "0r4fe0r"
	    ],
	    [
	        "ext.pageforms.select2",
	        "071cih1",
	        [
	            309,
	            75,
	            180
	        ]
	    ],
	    [
	        "ext.pageforms.fullcalendar.jquery1",
	        "0934qkc",
	        [
	            288,
	            303,
	            95
	        ]
	    ],
	    [
	        "ext.pageforms.fullcalendar.jquery3",
	        "02xh287",
	        [
	            288,
	            303,
	            95
	        ]
	    ],
	    [
	        "ext.pageforms.jsgrid",
	        "0hkn3je",
	        [
	            303,
	            181
	        ]
	    ],
	    [
	        "ext.pageforms.balloon",
	        "1hrpv1z"
	    ],
	    [
	        "ext.pageforms.wikieditor",
	        "0372jad"
	    ],
	    [
	        "ext.pageforms",
	        "0rcyb9n"
	    ],
	    [
	        "ext.pageforms.PF_CreateProperty",
	        "0nm8ltq"
	    ],
	    [
	        "ext.pageforms.PF_PageSchemas",
	        "16mdzqp"
	    ],
	    [
	        "ext.pageforms.PF_CreateTemplate",
	        "0apb8jh"
	    ],
	    [
	        "ext.pageforms.PF_CreateClass",
	        "0gh6v4r"
	    ],
	    [
	        "ext.pageforms.PF_CreateForm",
	        "0epuenf"
	    ],
	    [
	        "ext.categoryTree",
	        "0gltmvu",
	        [
	            101
	        ]
	    ],
	    [
	        "ext.categoryTree.css",
	        "0tfb3mb"
	    ],
	    [
	        "onoi.qtip.core",
	        "1yrve7q"
	    ],
	    [
	        "onoi.qtip.extended",
	        "1cd314z"
	    ],
	    [
	        "onoi.qtip",
	        "06sr3r6",
	        [
	            318
	        ]
	    ],
	    [
	        "onoi.md5",
	        "0p6c3eu"
	    ],
	    [
	        "onoi.blockUI",
	        "0nkru9b"
	    ],
	    [
	        "onoi.rangeslider",
	        "0enivvj"
	    ],
	    [
	        "onoi.localForage",
	        "0vhg5jf"
	    ],
	    [
	        "onoi.blobstore",
	        "08v4mmf",
	        [
	            323
	        ]
	    ],
	    [
	        "onoi.util",
	        "1abiiob",
	        [
	            320
	        ]
	    ],
	    [
	        "onoi.async",
	        "0xnyvpw"
	    ],
	    [
	        "onoi.jstorage",
	        "02vu1mx"
	    ],
	    [
	        "onoi.clipboard",
	        "10pbyuh"
	    ],
	    [
	        "onoi.bootstrap.tab.styles",
	        "1dbyhxz"
	    ],
	    [
	        "onoi.bootstrap.tab",
	        "0gkt4oo"
	    ],
	    [
	        "onoi.highlight",
	        "0mg91md"
	    ],
	    [
	        "onoi.dataTables.styles",
	        "16xph2j"
	    ],
	    [
	        "onoi.dataTables.searchHighlight",
	        "1s8h61j",
	        [
	            331
	        ]
	    ],
	    [
	        "onoi.dataTables.responsive",
	        "0gc9cga",
	        [
	            335
	        ]
	    ],
	    [
	        "onoi.dataTables",
	        "0lyxw58",
	        [
	            333
	        ]
	    ],
	    [
	        "ext.jquery.easing",
	        "1j3eqiw"
	    ],
	    [
	        "ext.jquery.fancybox",
	        "0o7voc0",
	        [
	            336,
	            343
	        ]
	    ],
	    [
	        "ext.jquery.multiselect",
	        "1exme00",
	        [
	            59,
	            79
	        ]
	    ],
	    [
	        "ext.jquery.multiselect.filter",
	        "0ifjlwh",
	        [
	            338
	        ]
	    ],
	    [
	        "ext.jquery.blockUI",
	        "1p0qp0l"
	    ],
	    [
	        "ext.jquery.jqgrid",
	        "0yfqan2",
	        [
	            343,
	            59
	        ]
	    ],
	    [
	        "ext.jquery.flot",
	        "1bbi6s3"
	    ],
	    [
	        "ext.jquery.migration.browser",
	        "0ge2jb9"
	    ],
	    [
	        "ext.srf",
	        "0ssgd6z",
	        [
	            448
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.api",
	        "1ynk96d",
	        [
	            344
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.util",
	        "0hzft65",
	        [
	            340,
	            344
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.widgets",
	        "15d5ffr",
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
	        "0kzvqdb",
	        [
	            341,
	            346,
	            77
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.jquery.sparkline",
	        "0ecy5nr",
	        [
	            343
	        ]
	    ],
	    [
	        "ext.srf.sparkline",
	        "1dtdljd",
	        [
	            349,
	            346
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.dygraphs.combined",
	        "0wimi58"
	    ],
	    [
	        "ext.srf.dygraphs",
	        "1mshb2s",
	        [
	            351,
	            453,
	            346,
	            20
	        ]
	    ],
	    [
	        "ext.jquery.listnav",
	        "187n384"
	    ],
	    [
	        "ext.jquery.listmenu",
	        "1abf4z6"
	    ],
	    [
	        "ext.jquery.pajinate",
	        "04xiwcf"
	    ],
	    [
	        "ext.srf.listwidget",
	        "1e3lu5n",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.srf.listwidget.alphabet",
	        "06sr3r6",
	        [
	            353,
	            356
	        ]
	    ],
	    [
	        "ext.srf.listwidget.menu",
	        "06sr3r6",
	        [
	            354,
	            356
	        ]
	    ],
	    [
	        "ext.srf.listwidget.pagination",
	        "06sr3r6",
	        [
	            355,
	            356
	        ]
	    ],
	    [
	        "ext.jquery.dynamiccarousel",
	        "0vmf269",
	        [
	            343
	        ]
	    ],
	    [
	        "ext.srf.pagewidget.carousel",
	        "1c93oil",
	        [
	            360,
	            346
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.core",
	        "02vhn2c",
	        [
	            343
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.excanvas",
	        "0zfqnyv"
	    ],
	    [
	        "ext.jquery.jqplot.json",
	        "1i6fsut"
	    ],
	    [
	        "ext.jquery.jqplot.cursor",
	        "19k9sd1"
	    ],
	    [
	        "ext.jquery.jqplot.logaxisrenderer",
	        "0q361lr"
	    ],
	    [
	        "ext.jquery.jqplot.mekko",
	        "155xjhz"
	    ],
	    [
	        "ext.jquery.jqplot.bar",
	        "0grg1d9",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.pie",
	        "09l6qbr",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.bubble",
	        "1381e4z",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.donut",
	        "08ajfo7",
	        [
	            369
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.pointlabels",
	        "1pzesfg",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.highlighter",
	        "1fj9jzv",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.enhancedlegend",
	        "0iauopm",
	        [
	            362
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.trendline",
	        "1ybc4vw"
	    ],
	    [
	        "ext.srf.jqplot.themes",
	        "1kdw87f",
	        [
	            27
	        ]
	    ],
	    [
	        "ext.srf.jqplot.cursor",
	        "06sr3r6",
	        [
	            365,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.enhancedlegend",
	        "06sr3r6",
	        [
	            374,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.pointlabels",
	        "06sr3r6",
	        [
	            372,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.highlighter",
	        "06sr3r6",
	        [
	            373,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.trendline",
	        "06sr3r6",
	        [
	            375,
	            383
	        ]
	    ],
	    [
	        "ext.srf.jqplot.chart",
	        "0v65sl0",
	        [
	            362,
	            376,
	            346,
	            20
	        ]
	    ],
	    [
	        "ext.srf.jqplot.bar",
	        "0oky33v",
	        [
	            368,
	            382
	        ]
	    ],
	    [
	        "ext.srf.jqplot.pie",
	        "10d07tp",
	        [
	            369,
	            382
	        ]
	    ],
	    [
	        "ext.srf.jqplot.bubble",
	        "1irxzz2",
	        [
	            370,
	            382
	        ]
	    ],
	    [
	        "ext.srf.jqplot.donut",
	        "10d07tp",
	        [
	            371,
	            382
	        ]
	    ],
	    [
	        "ext.smile.timeline.core",
	        "1c3v5bz"
	    ],
	    [
	        "ext.smile.timeline",
	        "1cy47rv"
	    ],
	    [
	        "ext.srf.timeline",
	        "1dlmefa",
	        [
	            388,
	            232
	        ]
	    ],
	    [
	        "ext.d3.core",
	        "0k3zkvw"
	    ],
	    [
	        "ext.srf.d3.common",
	        "04ncwn5",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.d3.wordcloud",
	        "1wvzh72",
	        [
	            390,
	            391
	        ]
	    ],
	    [
	        "ext.srf.d3.chart.treemap",
	        "1dum92w",
	        [
	            390,
	            391
	        ]
	    ],
	    [
	        "ext.srf.d3.chart.bubble",
	        "10mc8wd",
	        [
	            390,
	            391
	        ]
	    ],
	    [
	        "ext.srf.jquery.progressbar",
	        "0mco8yw"
	    ],
	    [
	        "ext.srf.jit",
	        "02quj7l"
	    ],
	    [
	        "ext.srf.jitgraph",
	        "0st5dth",
	        [
	            396,
	            395,
	            232
	        ]
	    ],
	    [
	        "ext.jquery.jcarousel",
	        "1md2393",
	        [
	            343
	        ]
	    ],
	    [
	        "ext.jquery.responsiveslides",
	        "14tefiu"
	    ],
	    [
	        "ext.srf.formats.gallery",
	        "1gdtxyf",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.srf.gallery.carousel",
	        "0fqeb7z",
	        [
	            398,
	            400
	        ]
	    ],
	    [
	        "ext.srf.gallery.slideshow",
	        "12n3a8n",
	        [
	            399,
	            400
	        ]
	    ],
	    [
	        "ext.srf.gallery.overlay",
	        "0f0hvh1",
	        [
	            337,
	            400
	        ]
	    ],
	    [
	        "ext.srf.gallery.redirect",
	        "06mjrp1",
	        [
	            400
	        ]
	    ],
	    [
	        "ext.jquery.fullcalendar",
	        "11gmxsh"
	    ],
	    [
	        "ext.jquery.gcal",
	        "13agv1l"
	    ],
	    [
	        "ext.srf.widgets.eventcalendar",
	        "17kcnc8",
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
	        "1f2vzut",
	        [
	            344
	        ]
	    ],
	    [
	        "ext.srf.eventcalendar",
	        "0f5mh4s",
	        [
	            405,
	            408,
	            407
	        ]
	    ],
	    [
	        "ext.srf.filtered",
	        "0wz4gp6",
	        [
	            344
	        ]
	    ],
	    [
	        "ext.srf.filtered.calendar-view.messages",
	        "1pkn5hj"
	    ],
	    [
	        "ext.srf.filtered.calendar-view",
	        "1q3maq0",
	        [
	            405,
	            411
	        ]
	    ],
	    [
	        "ext.srf.filtered.map-view.leaflet",
	        "09spoo1"
	    ],
	    [
	        "ext.srf.filtered.map-view",
	        "1vjappq"
	    ],
	    [
	        "ext.srf.filtered.value-filter",
	        "1lxh6wj"
	    ],
	    [
	        "ext.srf.filtered.value-filter.select",
	        "004egrz"
	    ],
	    [
	        "ext.srf.filtered.slider",
	        "08l97qs"
	    ],
	    [
	        "ext.srf.filtered.distance-filter",
	        "0so3gmv",
	        [
	            417
	        ]
	    ],
	    [
	        "ext.srf.filtered.number-filter",
	        "1jbcqux",
	        [
	            417
	        ]
	    ],
	    [
	        "ext.srf.slideshow",
	        "0nt5bpb",
	        [
	            153
	        ]
	    ],
	    [
	        "ext.jquery.tagcanvas",
	        "0ghscx3"
	    ],
	    [
	        "ext.srf.formats.tagcloud",
	        "0q3wuvm",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.srf.flot.core",
	        "09y82mm"
	    ],
	    [
	        "ext.srf.timeseries.flot",
	        "0gp3rgc",
	        [
	            342,
	            423,
	            346,
	            20
	        ]
	    ],
	    [
	        "ext.jquery.jplayer",
	        "0qwcmqy"
	    ],
	    [
	        "ext.jquery.jplayer.skin.blue.monday",
	        "0rblcq4"
	    ],
	    [
	        "ext.jquery.jplayer.skin.morning.light",
	        "0lz42dp"
	    ],
	    [
	        "ext.jquery.jplayer.playlist",
	        "0ovz8zo",
	        [
	            425
	        ]
	    ],
	    [
	        "ext.jquery.jplayer.inspector",
	        "07azbd2",
	        [
	            425
	        ]
	    ],
	    [
	        "ext.srf.template.jplayer",
	        "0eciuw0",
	        [
	            344
	        ]
	    ],
	    [
	        "ext.srf.formats.media",
	        "0kyfpmv",
	        [
	            428,
	            430
	        ],
	        "ext.srf"
	    ],
	    [
	        "jquery.dataTables",
	        "12z6a8w"
	    ],
	    [
	        "jquery.dataTables.extras",
	        "18ae4iv"
	    ],
	    [
	        "ext.srf.datatables",
	        "1hn4b5z",
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
	        "0s4wx2o",
	        [
	            434
	        ]
	    ],
	    [
	        "ext.srf.datatables.basic",
	        "1siyp21",
	        [
	            434
	        ]
	    ],
	    [
	        "MassEditRegex",
	        "0uucqul",
	        [
	            65,
	            180
	        ],
	        "MassEditRegex"
	    ],
	    [
	        "ext.smw",
	        "11sj1un",
	        [
	            441
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.style",
	        "1woup01",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.special.style",
	        "0ef0end",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.async",
	        "14hksnn",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.jStorage",
	        "1vf2k09",
	        [
	            94
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.md5",
	        "1ubqwsf",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.dataItem",
	        "14egq5u",
	        [
	            438,
	            141,
	            150
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.dataValue",
	        "175i1i5",
	        [
	            444
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.data",
	        "0gs20fy",
	        [
	            445
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.query",
	        "1f3su5c",
	        [
	            438,
	            153
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.api",
	        "1nc141z",
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
	        "1dgwe1k",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.qtip.styles",
	        "17arrom",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.qtip",
	        "1l1y4i9",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.tooltip.styles",
	        "0smlxhj",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.tooltip",
	        "11j3d9z",
	        [
	            451,
	            438,
	            452
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.tooltips",
	        "06sr3r6",
	        [
	            439,
	            453
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.autocomplete",
	        "0ttl296",
	        [
	            62
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.purge",
	        "165udhs",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.ask",
	        "0w10h23",
	        [
	            439,
	            453
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.browse.styles",
	        "067hep9",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.browse",
	        "0c84p1h",
	        [
	            439,
	            101
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.browse.page.autocomplete",
	        "06sr3r6",
	        [
	            455,
	            459
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.admin",
	        "1khhbv2",
	        [
	            101
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.property",
	        "1aoase5",
	        [
	            449,
	            153
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.pageforms.maps",
	        "0lyjtg8"
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
	script.src = "/wiki/load.php?debug=true&lang=en&modules=jquery%2Cmediawiki&only=scripts&skin=vector&version=0i4cm8w";
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
