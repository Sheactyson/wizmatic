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
	        "0wzhydq",
	        [
	            1
	        ]
	    ],
	    [
	        "site.styles",
	        "153brsj",
	        [],
	        "site"
	    ],
	    [
	        "noscript",
	        "0iel9f1",
	        [],
	        "noscript"
	    ],
	    [
	        "filepage",
	        "1fks11q"
	    ],
	    [
	        "user.groups",
	        "1s0a024",
	        [
	            5
	        ]
	    ],
	    [
	        "user",
	        "01aw07g",
	        [
	            6
	        ],
	        "user"
	    ],
	    [
	        "user.styles",
	        "0hd782y",
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
	        "1m6w9o4"
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
	        "0i5lwbc",
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
	        "1gyhtv3"
	    ],
	    [
	        "mediawiki.skinning.content",
	        "0sqowvq"
	    ],
	    [
	        "mediawiki.skinning.interface",
	        "087ow6j"
	    ],
	    [
	        "mediawiki.skinning.content.parsoid",
	        "1c0uyy1"
	    ],
	    [
	        "mediawiki.skinning.content.externallinks",
	        "1gka0zx"
	    ],
	    [
	        "jquery.accessKeyLabel",
	        "1sx0z0t",
	        [
	            27,
	            136
	        ]
	    ],
	    [
	        "jquery.appear",
	        "0xfyjdv"
	    ],
	    [
	        "jquery.arrowSteps",
	        "1wj5m3y"
	    ],
	    [
	        "jquery.async",
	        "1697wrf"
	    ],
	    [
	        "jquery.autoEllipsis",
	        "0gzogi1",
	        [
	            39
	        ]
	    ],
	    [
	        "jquery.badge",
	        "1hdawfa",
	        [
	            176
	        ]
	    ],
	    [
	        "jquery.byteLength",
	        "0yhocba"
	    ],
	    [
	        "jquery.byteLimit",
	        "1tpxk1l",
	        [
	            23
	        ]
	    ],
	    [
	        "jquery.checkboxShiftClick",
	        "060aa7x"
	    ],
	    [
	        "jquery.chosen",
	        "19anpzd"
	    ],
	    [
	        "jquery.client",
	        "1eemxps"
	    ],
	    [
	        "jquery.color",
	        "0kyn1hx",
	        [
	            29
	        ]
	    ],
	    [
	        "jquery.colorUtil",
	        "1yix7l5"
	    ],
	    [
	        "jquery.confirmable",
	        "1sdspli",
	        [
	            180
	        ]
	    ],
	    [
	        "jquery.cookie",
	        "02rvzp0"
	    ],
	    [
	        "jquery.expandableField",
	        "0rkezlx"
	    ],
	    [
	        "jquery.farbtastic",
	        "1s7xoxw",
	        [
	            29
	        ]
	    ],
	    [
	        "jquery.footHovzer",
	        "1e77ud8"
	    ],
	    [
	        "jquery.form",
	        "0o0vjcx"
	    ],
	    [
	        "jquery.fullscreen",
	        "1694w1x"
	    ],
	    [
	        "jquery.getAttrs",
	        "13liu26"
	    ],
	    [
	        "jquery.hidpi",
	        "12i0f3j"
	    ],
	    [
	        "jquery.highlightText",
	        "10j261r",
	        [
	            251,
	            136
	        ]
	    ],
	    [
	        "jquery.hoverIntent",
	        "11c6pv3"
	    ],
	    [
	        "jquery.i18n",
	        "1c34mn2",
	        [
	            178
	        ]
	    ],
	    [
	        "jquery.localize",
	        "1biz41t"
	    ],
	    [
	        "jquery.makeCollapsible",
	        "1gfb3cw"
	    ],
	    [
	        "jquery.mockjax",
	        "0tbnjfs"
	    ],
	    [
	        "jquery.mw-jump",
	        "1rlkht6"
	    ],
	    [
	        "jquery.mwExtension",
	        "16zseom"
	    ],
	    [
	        "jquery.placeholder",
	        "0j29izt"
	    ],
	    [
	        "jquery.qunit",
	        "0kifxss"
	    ],
	    [
	        "jquery.qunit.completenessTest",
	        "1560c70",
	        [
	            48
	        ]
	    ],
	    [
	        "jquery.spinner",
	        "1r6z46r"
	    ],
	    [
	        "jquery.jStorage",
	        "1oo0zsh",
	        [
	            94
	        ]
	    ],
	    [
	        "jquery.suggestions",
	        "0fr2n2a",
	        [
	            39
	        ]
	    ],
	    [
	        "jquery.tabIndex",
	        "0n2mmlf"
	    ],
	    [
	        "jquery.tablesorter",
	        "0oq8nf3",
	        [
	            251,
	            136,
	            181
	        ]
	    ],
	    [
	        "jquery.textSelection",
	        "1iywn7g",
	        [
	            27
	        ]
	    ],
	    [
	        "jquery.throttle-debounce",
	        "05uli2w"
	    ],
	    [
	        "jquery.xmldom",
	        "0dcyb77"
	    ],
	    [
	        "jquery.tipsy",
	        "0m82h1q"
	    ],
	    [
	        "jquery.ui.core",
	        "1j5effa",
	        [
	            60
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.core.styles",
	        "1pnfd0y",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.accordion",
	        "0zw03uw",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.autocomplete",
	        "04fwizl",
	        [
	            68
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.button",
	        "04vgzkg",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.datepicker",
	        "03yzoyn",
	        [
	            59
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.dialog",
	        "0hghxov",
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
	        "13gkejy",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.droppable",
	        "03op27v",
	        [
	            66
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.menu",
	        "009wvcu",
	        [
	            59,
	            70,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.mouse",
	        "1ycpsr2",
	        [
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.position",
	        "0nlq8fr",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.progressbar",
	        "1fp02nc",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.resizable",
	        "0pzrnxt",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.selectable",
	        "1eri132",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.slider",
	        "0nqt5ya",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.sortable",
	        "0g82wce",
	        [
	            59,
	            69
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.spinner",
	        "1z0vicm",
	        [
	            63
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.tabs",
	        "0a9q05x",
	        [
	            59,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.tooltip",
	        "0zzshbp",
	        [
	            59,
	            70,
	            79
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.ui.widget",
	        "0w72m5x",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.core",
	        "0sgo6f5",
	        [],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.blind",
	        "1bsrdf4",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.bounce",
	        "1x138f8",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.clip",
	        "02rn74l",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.drop",
	        "11epvxl",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.explode",
	        "14g25ey",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.fade",
	        "17a0yn4",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.fold",
	        "06qm5tw",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.highlight",
	        "1kssf6u",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.pulsate",
	        "0zv6xuu",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.scale",
	        "1a6pqrm",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.shake",
	        "0uadrld",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.slide",
	        "0p6vy5a",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "jquery.effects.transfer",
	        "1vfyyjw",
	        [
	            80
	        ],
	        "jquery.ui"
	    ],
	    [
	        "json",
	        "1wzbm2d",
	        [],
	        null,
	        null,
	        "/*!\n * Skip function for json2.js.\n */\nreturn !!( window.JSON \u0026\u0026 JSON.stringify \u0026\u0026 JSON.parse );\n"
	    ],
	    [
	        "moment",
	        "0k73kkn",
	        [
	            176
	        ]
	    ],
	    [
	        "mediawiki.apihelp",
	        "1eg7wlf"
	    ],
	    [
	        "mediawiki.template",
	        "0hv64gh"
	    ],
	    [
	        "mediawiki.template.mustache",
	        "0l6guiv",
	        [
	            97
	        ]
	    ],
	    [
	        "mediawiki.template.regexp",
	        "1npfy47",
	        [
	            97
	        ]
	    ],
	    [
	        "mediawiki.apipretty",
	        "084klin"
	    ],
	    [
	        "mediawiki.api",
	        "0r22yzk",
	        [
	            153,
	            10
	        ]
	    ],
	    [
	        "mediawiki.api.category",
	        "1qr2t2o",
	        [
	            141,
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.edit",
	        "0l9n4vu",
	        [
	            141,
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.login",
	        "1dq3z9w",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.options",
	        "1l7obar",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.parse",
	        "1ofie5d",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.upload",
	        "0gcr5t1",
	        [
	            251,
	            94,
	            103
	        ]
	    ],
	    [
	        "mediawiki.api.user",
	        "066ucoi",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.watch",
	        "1cj66o7",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.messages",
	        "12go2he",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.api.rollback",
	        "1kjbubo",
	        [
	            101
	        ]
	    ],
	    [
	        "mediawiki.content.json",
	        "14gvox9"
	    ],
	    [
	        "mediawiki.confirmCloseWindow",
	        "0e19lkt"
	    ],
	    [
	        "mediawiki.debug",
	        "1bsqxp0",
	        [
	            34
	        ]
	    ],
	    [
	        "mediawiki.diff.styles",
	        "0eqvl2k"
	    ],
	    [
	        "mediawiki.feedback",
	        "09fdh99",
	        [
	            141,
	            130,
	            260
	        ]
	    ],
	    [
	        "mediawiki.feedlink",
	        "1qxybxq"
	    ],
	    [
	        "mediawiki.filewarning",
	        "1co97u9",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.ForeignApi",
	        "0ic38vi",
	        [
	            120
	        ]
	    ],
	    [
	        "mediawiki.ForeignApi.core",
	        "1p0hqoh",
	        [
	            101,
	            252
	        ]
	    ],
	    [
	        "mediawiki.helplink",
	        "1p25lgw"
	    ],
	    [
	        "mediawiki.hidpi",
	        "0tgt78g",
	        [
	            38
	        ],
	        null,
	        null,
	        "/*!\n * Skip function for mediawiki.hdpi.js.\n */\nreturn 'srcset' in new Image();\n"
	    ],
	    [
	        "mediawiki.hlist",
	        "0cwfupv"
	    ],
	    [
	        "mediawiki.htmlform",
	        "140lq9x",
	        [
	            24,
	            136
	        ]
	    ],
	    [
	        "mediawiki.htmlform.ooui",
	        "1unnfdc",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.htmlform.styles",
	        "0i84zlo"
	    ],
	    [
	        "mediawiki.htmlform.ooui.styles",
	        "0v8nb0z"
	    ],
	    [
	        "mediawiki.icon",
	        "012or7q"
	    ],
	    [
	        "mediawiki.inspect",
	        "12lmgel",
	        [
	            23,
	            94,
	            136
	        ]
	    ],
	    [
	        "mediawiki.messagePoster",
	        "1xgjlji",
	        [
	            119
	        ]
	    ],
	    [
	        "mediawiki.messagePoster.wikitext",
	        "1ebm9qs",
	        [
	            103,
	            130
	        ]
	    ],
	    [
	        "mediawiki.notification",
	        "0u8be4y",
	        [
	            189
	        ]
	    ],
	    [
	        "mediawiki.notify",
	        "1bzk9mg"
	    ],
	    [
	        "mediawiki.notification.convertmessagebox",
	        "1bh8dhx",
	        [
	            132
	        ]
	    ],
	    [
	        "mediawiki.notification.convertmessagebox.styles",
	        "1z053ue"
	    ],
	    [
	        "mediawiki.RegExp",
	        "16d93q6"
	    ],
	    [
	        "mediawiki.pager.tablePager",
	        "1ir8gjq"
	    ],
	    [
	        "mediawiki.searchSuggest",
	        "0n85b2g",
	        [
	            37,
	            47,
	            52,
	            101
	        ]
	    ],
	    [
	        "mediawiki.sectionAnchor",
	        "1s1gwgw"
	    ],
	    [
	        "mediawiki.storage",
	        "0n7jgay"
	    ],
	    [
	        "mediawiki.Title",
	        "035s4b1",
	        [
	            23,
	            153
	        ]
	    ],
	    [
	        "mediawiki.Upload",
	        "166n2t7",
	        [
	            107
	        ]
	    ],
	    [
	        "mediawiki.ForeignUpload",
	        "1b0so60",
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
	        "1h67ynn",
	        [
	            144,
	            143
	        ]
	    ],
	    [
	        "mediawiki.Upload.Dialog",
	        "09qr8l0",
	        [
	            147
	        ]
	    ],
	    [
	        "mediawiki.Upload.BookletLayout",
	        "0yq60ms",
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
	        "0l889qe",
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
	        "0fwrnhi",
	        [
	            157
	        ]
	    ],
	    [
	        "mediawiki.Uri",
	        "0z1tggf",
	        [
	            153,
	            99
	        ]
	    ],
	    [
	        "mediawiki.user",
	        "09oxthg",
	        [
	            108,
	            157,
	            9
	        ]
	    ],
	    [
	        "mediawiki.userSuggest",
	        "1792jyv",
	        [
	            52,
	            101
	        ]
	    ],
	    [
	        "mediawiki.util",
	        "010hg8s",
	        [
	            17,
	            133
	        ]
	    ],
	    [
	        "mediawiki.viewport",
	        "11ea0vg"
	    ],
	    [
	        "mediawiki.checkboxtoggle",
	        "1p773wh"
	    ],
	    [
	        "mediawiki.checkboxtoggle.styles",
	        "12c6lat"
	    ],
	    [
	        "mediawiki.cookie",
	        "1mtocdq",
	        [
	            31
	        ]
	    ],
	    [
	        "mediawiki.toolbar",
	        "1x86tor",
	        [
	            55
	        ]
	    ],
	    [
	        "mediawiki.experiments",
	        "1bdamfk"
	    ],
	    [
	        "mediawiki.action.edit",
	        "0aleo3k",
	        [
	            24,
	            55,
	            161,
	            101
	        ]
	    ],
	    [
	        "mediawiki.action.edit.styles",
	        "0qlcm33"
	    ],
	    [
	        "mediawiki.action.edit.collapsibleFooter",
	        "0j9ezm5",
	        [
	            43,
	            157,
	            128
	        ]
	    ],
	    [
	        "mediawiki.action.edit.preview",
	        "069pulu",
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
	        "0feia2h"
	    ],
	    [
	        "mediawiki.action.history.styles",
	        "0jx93k5"
	    ],
	    [
	        "mediawiki.action.history.diff",
	        "0eqvl2k"
	    ],
	    [
	        "mediawiki.action.view.dblClickEdit",
	        "1lg2wbu",
	        [
	            189,
	            9
	        ]
	    ],
	    [
	        "mediawiki.action.view.metadata",
	        "1dum0xq"
	    ],
	    [
	        "mediawiki.action.view.categoryPage.styles",
	        "167895x"
	    ],
	    [
	        "mediawiki.action.view.postEdit",
	        "09l9d9y",
	        [
	            157,
	            180,
	            97
	        ]
	    ],
	    [
	        "mediawiki.action.view.redirect",
	        "0js04qf",
	        [
	            27
	        ]
	    ],
	    [
	        "mediawiki.action.view.redirectPage",
	        "0vy4s33"
	    ],
	    [
	        "mediawiki.action.view.rightClickEdit",
	        "1citu9y"
	    ],
	    [
	        "mediawiki.action.edit.editWarning",
	        "0stqp2u",
	        [
	            55,
	            113,
	            180
	        ]
	    ],
	    [
	        "mediawiki.action.view.filepage",
	        "0aktmka"
	    ],
	    [
	        "mediawiki.language",
	        "02aex32",
	        [
	            177,
	            11
	        ]
	    ],
	    [
	        "mediawiki.cldr",
	        "1iaik6x",
	        [
	            178
	        ]
	    ],
	    [
	        "mediawiki.libs.pluralruleparser",
	        "00cbvcf"
	    ],
	    [
	        "mediawiki.language.init",
	        "18nya42"
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
	        "191s62t",
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
	        "1mfytcq"
	    ],
	    [
	        "mediawiki.page.gallery",
	        "1ckv4yt",
	        [
	            56,
	            186
	        ]
	    ],
	    [
	        "mediawiki.page.gallery.styles",
	        "0799dvb"
	    ],
	    [
	        "mediawiki.page.gallery.slideshow",
	        "1qeos7l",
	        [
	            141,
	            101,
	            258,
	            274
	        ]
	    ],
	    [
	        "mediawiki.page.ready",
	        "063edpt",
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
	        "06f0dbw",
	        [
	            153
	        ]
	    ],
	    [
	        "mediawiki.page.patrol.ajax",
	        "1p5nggk",
	        [
	            50,
	            141,
	            101,
	            189
	        ]
	    ],
	    [
	        "mediawiki.page.watch.ajax",
	        "1bbohe4",
	        [
	            109,
	            189
	        ]
	    ],
	    [
	        "mediawiki.page.rollback",
	        "1tbfzle",
	        [
	            50,
	            111
	        ]
	    ],
	    [
	        "mediawiki.page.image.pagination",
	        "0otlskz",
	        [
	            50,
	            153
	        ]
	    ],
	    [
	        "mediawiki.special",
	        "0owbntf"
	    ],
	    [
	        "mediawiki.special.apisandbox.styles",
	        "1hkn8pr"
	    ],
	    [
	        "mediawiki.special.apisandbox",
	        "07w955k",
	        [
	            101,
	            180,
	            244,
	            255
	        ]
	    ],
	    [
	        "mediawiki.special.block",
	        "1jg1kfy",
	        [
	            153
	        ]
	    ],
	    [
	        "mediawiki.special.changeslist",
	        "1m6bw7q"
	    ],
	    [
	        "mediawiki.special.changeslist.legend",
	        "1luf7en"
	    ],
	    [
	        "mediawiki.special.changeslist.legend.js",
	        "08xuzo9",
	        [
	            43,
	            157
	        ]
	    ],
	    [
	        "mediawiki.special.changeslist.enhanced",
	        "0zo7eyq"
	    ],
	    [
	        "mediawiki.special.changeslist.visitedstatus",
	        "1pf753r"
	    ],
	    [
	        "mediawiki.special.comparepages.styles",
	        "1bdy0nd"
	    ],
	    [
	        "mediawiki.special.edittags",
	        "12o33zi",
	        [
	            26
	        ]
	    ],
	    [
	        "mediawiki.special.edittags.styles",
	        "1qthwjp"
	    ],
	    [
	        "mediawiki.special.import",
	        "06qmfrs"
	    ],
	    [
	        "mediawiki.special.movePage",
	        "1829sbl",
	        [
	            241
	        ]
	    ],
	    [
	        "mediawiki.special.movePage.styles",
	        "15ho2uh"
	    ],
	    [
	        "mediawiki.special.pageLanguage",
	        "0yo4s91",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.special.pagesWithProp",
	        "1rzq8c6"
	    ],
	    [
	        "mediawiki.special.preferences",
	        "0hn8kvy",
	        [
	            113,
	            176,
	            134
	        ]
	    ],
	    [
	        "mediawiki.special.userrights",
	        "1qwnvex",
	        [
	            134
	        ]
	    ],
	    [
	        "mediawiki.special.preferences.styles",
	        "1l603o9"
	    ],
	    [
	        "mediawiki.special.recentchanges",
	        "1l55k0l"
	    ],
	    [
	        "mediawiki.special.search",
	        "0vtrx0u",
	        [
	            247
	        ]
	    ],
	    [
	        "mediawiki.special.search.styles",
	        "1a933lp"
	    ],
	    [
	        "mediawiki.special.undelete",
	        "0xy2g2g"
	    ],
	    [
	        "mediawiki.special.upload",
	        "06q6uk4",
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
	        "1l2s36g"
	    ],
	    [
	        "mediawiki.special.userlogin.common.styles",
	        "17wjnqr"
	    ],
	    [
	        "mediawiki.special.userlogin.signup.styles",
	        "1gkl8wt"
	    ],
	    [
	        "mediawiki.special.userlogin.login.styles",
	        "0ckrcf3"
	    ],
	    [
	        "mediawiki.special.userlogin.signup.js",
	        "17kbu65",
	        [
	            56,
	            101,
	            180
	        ]
	    ],
	    [
	        "mediawiki.special.unwatchedPages",
	        "1okqu4u",
	        [
	            141,
	            109
	        ]
	    ],
	    [
	        "mediawiki.special.watchlist",
	        "0rf7584"
	    ],
	    [
	        "mediawiki.special.version",
	        "19ndxwi"
	    ],
	    [
	        "mediawiki.legacy.config",
	        "1sofvhn"
	    ],
	    [
	        "mediawiki.legacy.commonPrint",
	        "1t78igj"
	    ],
	    [
	        "mediawiki.legacy.protect",
	        "1ogepyv",
	        [
	            24
	        ]
	    ],
	    [
	        "mediawiki.legacy.shared",
	        "17fw73w"
	    ],
	    [
	        "mediawiki.legacy.oldshared",
	        "1xfwt6c"
	    ],
	    [
	        "mediawiki.legacy.wikibits",
	        "0qx2xis",
	        [
	            153
	        ]
	    ],
	    [
	        "mediawiki.ui",
	        "130auzf"
	    ],
	    [
	        "mediawiki.ui.checkbox",
	        "03uogvk"
	    ],
	    [
	        "mediawiki.ui.radio",
	        "0qlg141"
	    ],
	    [
	        "mediawiki.ui.anchor",
	        "11cavxi"
	    ],
	    [
	        "mediawiki.ui.button",
	        "0khgnok"
	    ],
	    [
	        "mediawiki.ui.input",
	        "1ji3xy9"
	    ],
	    [
	        "mediawiki.ui.icon",
	        "0np1ace"
	    ],
	    [
	        "mediawiki.ui.text",
	        "00c86l1"
	    ],
	    [
	        "mediawiki.widgets",
	        "1cnshz0",
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
	        "1h2tl3z"
	    ],
	    [
	        "mediawiki.widgets.DateInputWidget",
	        "0tng86d",
	        [
	            95,
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.datetime",
	        "0a9kzsa",
	        [
	            256
	        ]
	    ],
	    [
	        "mediawiki.widgets.CategorySelector",
	        "1txwbh3",
	        [
	            119,
	            141,
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.UserInputWidget",
	        "1pzdezt",
	        [
	            258
	        ]
	    ],
	    [
	        "mediawiki.widgets.SearchInputWidget",
	        "1kels7r",
	        [
	            138,
	            241
	        ]
	    ],
	    [
	        "mediawiki.widgets.SearchInputWidget.styles",
	        "137rgad"
	    ],
	    [
	        "mediawiki.widgets.StashedFileWidget",
	        "0i2ik4b",
	        [
	            256
	        ]
	    ],
	    [
	        "es5-shim",
	        "0fmueqn",
	        [],
	        null,
	        null,
	        "/*!\n * Skip function for es5-shim module.\n *\n * Test for strict mode as a proxy for full ES5 function support (but not syntax)\n * Per http://kangax.github.io/compat-table/es5/ this is a reasonable shortcut\n * that still allows this to be as short as possible (there are no browsers we\n * support that have strict mode, but lack other features).\n *\n * Do explicitly test for Function#bind because of PhantomJS (which implements\n * strict mode, but lacks Function#bind).\n *\n * IE9 supports all features except strict mode, so loading es5-shim should be close to\n * a no-op but does increase page payload).\n */\nreturn ( function () {\n\t'use strict';\n\treturn !this \u0026\u0026 !!Function.prototype.bind;\n}() );\n"
	    ],
	    [
	        "dom-level2-shim",
	        "1y4dqk1",
	        [],
	        null,
	        null,
	        "/*!\n * Skip function for dom-level2-shim module.\n *\n * Tests for window.Node because that's the only thing that this shim is adding.\n */\nreturn !!window.Node;\n"
	    ],
	    [
	        "oojs",
	        "1nqnmrc",
	        [
	            250,
	            94
	        ]
	    ],
	    [
	        "mediawiki.router",
	        "0918cpr",
	        [
	            254
	        ]
	    ],
	    [
	        "oojs-router",
	        "0e85q85",
	        [
	            252
	        ]
	    ],
	    [
	        "oojs-ui",
	        "1s0a024",
	        [
	            259,
	            258,
	            260
	        ]
	    ],
	    [
	        "oojs-ui-core",
	        "1rhhwbr",
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
	        "129out8"
	    ],
	    [
	        "oojs-ui-widgets",
	        "1rejgjn",
	        [
	            256
	        ]
	    ],
	    [
	        "oojs-ui-toolbars",
	        "128b0f2",
	        [
	            256
	        ]
	    ],
	    [
	        "oojs-ui-windows",
	        "12ky7xo",
	        [
	            256
	        ]
	    ],
	    [
	        "oojs-ui.styles.icons",
	        "0fnb8yy"
	    ],
	    [
	        "oojs-ui.styles.indicators",
	        "1mc1986"
	    ],
	    [
	        "oojs-ui.styles.textures",
	        "0mpgy8a"
	    ],
	    [
	        "oojs-ui.styles.icons-accessibility",
	        "15g3vdg"
	    ],
	    [
	        "oojs-ui.styles.icons-alerts",
	        "1mxke8l"
	    ],
	    [
	        "oojs-ui.styles.icons-content",
	        "1vbe83x"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-advanced",
	        "1mjo8jq"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-core",
	        "112auai"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-list",
	        "038xwrf"
	    ],
	    [
	        "oojs-ui.styles.icons-editing-styling",
	        "0okcjcm"
	    ],
	    [
	        "oojs-ui.styles.icons-interactions",
	        "0wcabne"
	    ],
	    [
	        "oojs-ui.styles.icons-layout",
	        "1w9lh72"
	    ],
	    [
	        "oojs-ui.styles.icons-location",
	        "12n7ko2"
	    ],
	    [
	        "oojs-ui.styles.icons-media",
	        "1gm4l0h"
	    ],
	    [
	        "oojs-ui.styles.icons-moderation",
	        "1b7g4xb"
	    ],
	    [
	        "oojs-ui.styles.icons-movement",
	        "0nb6ari"
	    ],
	    [
	        "oojs-ui.styles.icons-user",
	        "0bgww1g"
	    ],
	    [
	        "oojs-ui.styles.icons-wikimedia",
	        "14byml2"
	    ],
	    [
	        "skins.vector.styles",
	        "0nfw0ym"
	    ],
	    [
	        "skins.vector.styles.responsive",
	        "0yowwvn"
	    ],
	    [
	        "skins.vector.js",
	        "14j4a7y",
	        [
	            53,
	            56
	        ]
	    ],
	    [
	        "ext.tabs",
	        "1hqz37s"
	    ],
	    [
	        "ext.collapsiblevector.collapsibleNav",
	        "0idrg9n",
	        [
	            27,
	            31
	        ]
	    ],
	    [
	        "ext.pageforms.main",
	        "0pgy9eg",
	        [
	            291,
	            304,
	            290,
	            309,
	            62,
	            101
	        ]
	    ],
	    [
	        "ext.pageforms.browser",
	        "0yauxvw"
	    ],
	    [
	        "ext.pageforms.fancybox.jquery1",
	        "1iy1tlt",
	        [
	            285
	        ]
	    ],
	    [
	        "ext.pageforms.fancybox.jquery3",
	        "08fhfzo",
	        [
	            285
	        ]
	    ],
	    [
	        "ext.pageforms.fancytree.dep",
	        "0a1u5m7"
	    ],
	    [
	        "ext.pageforms.fancytree",
	        "1g9w6it",
	        [
	            288,
	            70,
	            79
	        ]
	    ],
	    [
	        "ext.pageforms.sortable",
	        "1ga4uib"
	    ],
	    [
	        "ext.pageforms.autogrow",
	        "0vykorp"
	    ],
	    [
	        "ext.pageforms.popupformedit",
	        "04nqk9x",
	        [
	            285
	        ]
	    ],
	    [
	        "ext.pageforms.autoedit",
	        "0eauj5z"
	    ],
	    [
	        "ext.pageforms.submit",
	        "0gb06lm"
	    ],
	    [
	        "ext.pageforms.collapsible",
	        "1gpa91k"
	    ],
	    [
	        "ext.pageforms.imagepreview",
	        "0q2mem6"
	    ],
	    [
	        "ext.pageforms.checkboxes",
	        "0e72bzd"
	    ],
	    [
	        "ext.pageforms.datepicker",
	        "0d80zrx",
	        [
	            284,
	            64
	        ]
	    ],
	    [
	        "ext.pageforms.timepicker",
	        "01zr0hg"
	    ],
	    [
	        "ext.pageforms.datetimepicker",
	        "0bdwrr5",
	        [
	            298,
	            299
	        ]
	    ],
	    [
	        "ext.pageforms.regexp",
	        "1hxpbmn",
	        [
	            284
	        ]
	    ],
	    [
	        "ext.pageforms.rating",
	        "0mgtgdu"
	    ],
	    [
	        "ext.pageforms.simpleupload",
	        "13th5t5"
	    ],
	    [
	        "ext.pageforms.select2",
	        "06nv74z",
	        [
	            310,
	            75,
	            180
	        ]
	    ],
	    [
	        "ext.pageforms.fullcalendar.jquery1",
	        "04abkcy",
	        [
	            289,
	            304,
	            95
	        ]
	    ],
	    [
	        "ext.pageforms.fullcalendar.jquery3",
	        "19y0cqp",
	        [
	            289,
	            304,
	            95
	        ]
	    ],
	    [
	        "ext.pageforms.jsgrid",
	        "0i21ooo",
	        [
	            304,
	            181
	        ]
	    ],
	    [
	        "ext.pageforms.balloon",
	        "0ogd049"
	    ],
	    [
	        "ext.pageforms.wikieditor",
	        "17juds3"
	    ],
	    [
	        "ext.pageforms",
	        "1lbkfrp"
	    ],
	    [
	        "ext.pageforms.PF_CreateProperty",
	        "0hhsqkc"
	    ],
	    [
	        "ext.pageforms.PF_PageSchemas",
	        "0vj0z9r"
	    ],
	    [
	        "ext.pageforms.PF_CreateTemplate",
	        "0qagtc3"
	    ],
	    [
	        "ext.pageforms.PF_CreateClass",
	        "0nnciqd"
	    ],
	    [
	        "ext.pageforms.PF_CreateForm",
	        "0106di9"
	    ],
	    [
	        "ext.inputBox.styles",
	        "1ej4jnm"
	    ],
	    [
	        "ext.inputBox",
	        "0eto92l",
	        [
	            56
	        ]
	    ],
	    [
	        "ext.categoryTree",
	        "1adkads",
	        [
	            101
	        ]
	    ],
	    [
	        "ext.categoryTree.css",
	        "0jusozl"
	    ],
	    [
	        "onoi.qtip.core",
	        "0r85ahk"
	    ],
	    [
	        "onoi.qtip.extended",
	        "12n3zbx"
	    ],
	    [
	        "onoi.qtip",
	        "1s0a024",
	        [
	            321
	        ]
	    ],
	    [
	        "onoi.md5",
	        "1h2y08k"
	    ],
	    [
	        "onoi.blockUI",
	        "0cnu5nl"
	    ],
	    [
	        "onoi.rangeslider",
	        "0btu8p1"
	    ],
	    [
	        "onoi.localForage",
	        "0hv1d9t"
	    ],
	    [
	        "onoi.blobstore",
	        "0n7lzcl",
	        [
	            326
	        ]
	    ],
	    [
	        "onoi.util",
	        "0gqe2zd",
	        [
	            323
	        ]
	    ],
	    [
	        "onoi.async",
	        "023h5d6"
	    ],
	    [
	        "onoi.jstorage",
	        "00e4pdz"
	    ],
	    [
	        "onoi.clipboard",
	        "1qtib33"
	    ],
	    [
	        "onoi.bootstrap.tab.styles",
	        "1rjwy2l"
	    ],
	    [
	        "onoi.bootstrap.tab",
	        "0a1j4ye"
	    ],
	    [
	        "onoi.highlight",
	        "1rzag43"
	    ],
	    [
	        "onoi.dataTables.styles",
	        "0iiccn5"
	    ],
	    [
	        "onoi.dataTables.searchHighlight",
	        "1b1k38x",
	        [
	            334
	        ]
	    ],
	    [
	        "onoi.dataTables.responsive",
	        "0vdhbz8",
	        [
	            338
	        ]
	    ],
	    [
	        "onoi.dataTables",
	        "05p3v1e",
	        [
	            336
	        ]
	    ],
	    [
	        "ext.jquery.easing",
	        "17zva2q"
	    ],
	    [
	        "ext.jquery.fancybox",
	        "091vnve",
	        [
	            339,
	            346
	        ]
	    ],
	    [
	        "ext.jquery.multiselect",
	        "053b5pu",
	        [
	            59,
	            79
	        ]
	    ],
	    [
	        "ext.jquery.multiselect.filter",
	        "19rdd0z",
	        [
	            341
	        ]
	    ],
	    [
	        "ext.jquery.blockUI",
	        "0c2tvqf"
	    ],
	    [
	        "ext.jquery.jqgrid",
	        "061y55c",
	        [
	            346,
	            59
	        ]
	    ],
	    [
	        "ext.jquery.flot",
	        "0fx37qt"
	    ],
	    [
	        "ext.jquery.migration.browser",
	        "1c5dwsz"
	    ],
	    [
	        "ext.srf",
	        "0ldr0ip",
	        [
	            451
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.api",
	        "0aa9fab",
	        [
	            347
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.util",
	        "0givmyf",
	        [
	            343,
	            347
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.widgets",
	        "0x67w7x",
	        [
	            341,
	            347,
	            63,
	            74
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.srf.util.grid",
	        "08qnfwh",
	        [
	            344,
	            349,
	            77
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.jquery.sparkline",
	        "0rx41jd",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.srf.sparkline",
	        "0602lxj",
	        [
	            352,
	            349
	        ],
	        "ext.srf"
	    ],
	    [
	        "ext.dygraphs.combined",
	        "0k6kpv2"
	    ],
	    [
	        "ext.srf.dygraphs",
	        "1bcwnxm",
	        [
	            354,
	            456,
	            349,
	            20
	        ]
	    ],
	    [
	        "ext.jquery.listnav",
	        "1iqahke"
	    ],
	    [
	        "ext.jquery.listmenu",
	        "0nk8hp4"
	    ],
	    [
	        "ext.jquery.pajinate",
	        "1ax5vo1"
	    ],
	    [
	        "ext.srf.listwidget",
	        "02ibujp",
	        [
	            349
	        ]
	    ],
	    [
	        "ext.srf.listwidget.alphabet",
	        "1s0a024",
	        [
	            356,
	            359
	        ]
	    ],
	    [
	        "ext.srf.listwidget.menu",
	        "1s0a024",
	        [
	            357,
	            359
	        ]
	    ],
	    [
	        "ext.srf.listwidget.pagination",
	        "1s0a024",
	        [
	            358,
	            359
	        ]
	    ],
	    [
	        "ext.jquery.dynamiccarousel",
	        "12xsntn",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.srf.pagewidget.carousel",
	        "09xqkiv",
	        [
	            363,
	            349
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.core",
	        "13zntaq",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.excanvas",
	        "09ldyvl"
	    ],
	    [
	        "ext.jquery.jqplot.json",
	        "0xc360f"
	    ],
	    [
	        "ext.jquery.jqplot.cursor",
	        "1mpj417"
	    ],
	    [
	        "ext.jquery.jqplot.logaxisrenderer",
	        "0hn208t"
	    ],
	    [
	        "ext.jquery.jqplot.mekko",
	        "1jz162l"
	    ],
	    [
	        "ext.jquery.jqplot.bar",
	        "0ax9hyz",
	        [
	            365
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.pie",
	        "0kmgr31",
	        [
	            365
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.bubble",
	        "0aqhey1",
	        [
	            365
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.donut",
	        "1ilpkt5",
	        [
	            372
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.pointlabels",
	        "0nd8v5m",
	        [
	            365
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.highlighter",
	        "0db2wdt",
	        [
	            365
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.enhancedlegend",
	        "0lpgpj8",
	        [
	            365
	        ]
	    ],
	    [
	        "ext.jquery.jqplot.trendline",
	        "0o9qm3q"
	    ],
	    [
	        "ext.srf.jqplot.themes",
	        "1164mj5",
	        [
	            27
	        ]
	    ],
	    [
	        "ext.srf.jqplot.cursor",
	        "1s0a024",
	        [
	            368,
	            386
	        ]
	    ],
	    [
	        "ext.srf.jqplot.enhancedlegend",
	        "1s0a024",
	        [
	            377,
	            386
	        ]
	    ],
	    [
	        "ext.srf.jqplot.pointlabels",
	        "1s0a024",
	        [
	            375,
	            386
	        ]
	    ],
	    [
	        "ext.srf.jqplot.highlighter",
	        "1s0a024",
	        [
	            376,
	            386
	        ]
	    ],
	    [
	        "ext.srf.jqplot.trendline",
	        "1s0a024",
	        [
	            378,
	            386
	        ]
	    ],
	    [
	        "ext.srf.jqplot.chart",
	        "0jpjvee",
	        [
	            365,
	            379,
	            349,
	            20
	        ]
	    ],
	    [
	        "ext.srf.jqplot.bar",
	        "0jy1q69",
	        [
	            371,
	            385
	        ]
	    ],
	    [
	        "ext.srf.jqplot.pie",
	        "0tiguur",
	        [
	            372,
	            385
	        ]
	    ],
	    [
	        "ext.srf.jqplot.bubble",
	        "14u7ls8",
	        [
	            373,
	            385
	        ]
	    ],
	    [
	        "ext.srf.jqplot.donut",
	        "0tiguur",
	        [
	            374,
	            385
	        ]
	    ],
	    [
	        "ext.smile.timeline.core",
	        "189qayh"
	    ],
	    [
	        "ext.smile.timeline",
	        "0rvxj29"
	    ],
	    [
	        "ext.srf.timeline",
	        "1mhqbs4",
	        [
	            391,
	            232
	        ]
	    ],
	    [
	        "ext.d3.core",
	        "17lf4mm"
	    ],
	    [
	        "ext.srf.d3.common",
	        "06w5bc3",
	        [
	            349
	        ]
	    ],
	    [
	        "ext.d3.wordcloud",
	        "1qvfjt0",
	        [
	            393,
	            394
	        ]
	    ],
	    [
	        "ext.srf.d3.chart.treemap",
	        "0njx8we",
	        [
	            393,
	            394
	        ]
	    ],
	    [
	        "ext.srf.d3.chart.bubble",
	        "0u2xti7",
	        [
	            393,
	            394
	        ]
	    ],
	    [
	        "ext.srf.jquery.progressbar",
	        "0m1tq86"
	    ],
	    [
	        "ext.srf.jit",
	        "0g1itc3"
	    ],
	    [
	        "ext.srf.jitgraph",
	        "0yyj45v",
	        [
	            399,
	            398,
	            232
	        ]
	    ],
	    [
	        "ext.jquery.jcarousel",
	        "09tsx05",
	        [
	            346
	        ]
	    ],
	    [
	        "ext.jquery.responsiveslides",
	        "0z4cek4"
	    ],
	    [
	        "ext.srf.formats.gallery",
	        "0y7g045",
	        [
	            349
	        ]
	    ],
	    [
	        "ext.srf.gallery.carousel",
	        "1nirc8d",
	        [
	            401,
	            403
	        ]
	    ],
	    [
	        "ext.srf.gallery.slideshow",
	        "1nx6iod",
	        [
	            402,
	            403
	        ]
	    ],
	    [
	        "ext.srf.gallery.overlay",
	        "0femz6r",
	        [
	            340,
	            403
	        ]
	    ],
	    [
	        "ext.srf.gallery.redirect",
	        "0jlp933",
	        [
	            403
	        ]
	    ],
	    [
	        "ext.jquery.fullcalendar",
	        "12yv5c3"
	    ],
	    [
	        "ext.jquery.gcal",
	        "1vtqtcr"
	    ],
	    [
	        "ext.srf.widgets.eventcalendar",
	        "0ddnbp6",
	        [
	            456,
	            348,
	            349,
	            64,
	            74
	        ]
	    ],
	    [
	        "ext.srf.hooks.eventcalendar",
	        "15uk8dj",
	        [
	            347
	        ]
	    ],
	    [
	        "ext.srf.eventcalendar",
	        "14twqc2",
	        [
	            408,
	            411,
	            410
	        ]
	    ],
	    [
	        "ext.srf.filtered",
	        "0y497c8",
	        [
	            347
	        ]
	    ],
	    [
	        "ext.srf.filtered.calendar-view.messages",
	        "0u0dxel"
	    ],
	    [
	        "ext.srf.filtered.calendar-view",
	        "1dwfpfm",
	        [
	            408,
	            414
	        ]
	    ],
	    [
	        "ext.srf.filtered.map-view.leaflet",
	        "1k2q0pb"
	    ],
	    [
	        "ext.srf.filtered.map-view",
	        "110oi88"
	    ],
	    [
	        "ext.srf.filtered.value-filter",
	        "0114iut"
	    ],
	    [
	        "ext.srf.filtered.value-filter.select",
	        "0xl2zpp"
	    ],
	    [
	        "ext.srf.filtered.slider",
	        "1xsbb2u"
	    ],
	    [
	        "ext.srf.filtered.distance-filter",
	        "0h85fxx",
	        [
	            420
	        ]
	    ],
	    [
	        "ext.srf.filtered.number-filter",
	        "0adbzc3",
	        [
	            420
	        ]
	    ],
	    [
	        "ext.srf.slideshow",
	        "1v1dj45",
	        [
	            153
	        ]
	    ],
	    [
	        "ext.jquery.tagcanvas",
	        "1mex8rx"
	    ],
	    [
	        "ext.srf.formats.tagcloud",
	        "1sk9m7o",
	        [
	            349
	        ]
	    ],
	    [
	        "ext.srf.flot.core",
	        "0d92884"
	    ],
	    [
	        "ext.srf.timeseries.flot",
	        "0ykdgie",
	        [
	            345,
	            426,
	            349,
	            20
	        ]
	    ],
	    [
	        "ext.jquery.jplayer",
	        "0nj5z3w"
	    ],
	    [
	        "ext.jquery.jplayer.skin.blue.monday",
	        "0p4f2dm"
	    ],
	    [
	        "ext.jquery.jplayer.skin.morning.light",
	        "0hdqzh7"
	    ],
	    [
	        "ext.jquery.jplayer.playlist",
	        "1lrvxgq",
	        [
	            428
	        ]
	    ],
	    [
	        "ext.jquery.jplayer.inspector",
	        "1os23nw",
	        [
	            428
	        ]
	    ],
	    [
	        "ext.srf.template.jplayer",
	        "117h2ou",
	        [
	            347
	        ]
	    ],
	    [
	        "ext.srf.formats.media",
	        "08hjmmx",
	        [
	            431,
	            433
	        ],
	        "ext.srf"
	    ],
	    [
	        "jquery.dataTables",
	        "1m7bthq"
	    ],
	    [
	        "jquery.dataTables.extras",
	        "075uynd"
	    ],
	    [
	        "ext.srf.datatables",
	        "11id4wh",
	        [
	            348,
	            349,
	            350,
	            435,
	            436
	        ]
	    ],
	    [
	        "ext.srf.datatables.bootstrap",
	        "141edvq",
	        [
	            437
	        ]
	    ],
	    [
	        "ext.srf.datatables.basic",
	        "0ix5zfn",
	        [
	            437
	        ]
	    ],
	    [
	        "MassEditRegex",
	        "0c83r3n",
	        [
	            65,
	            180
	        ],
	        "MassEditRegex"
	    ],
	    [
	        "ext.smw",
	        "01hoich",
	        [
	            444
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.style",
	        "1ljtzsn",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.special.style",
	        "0g823if",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.async",
	        "0bk93ct",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.jStorage",
	        "1isljo3",
	        [
	            94
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.md5",
	        "0ey4gih",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.dataItem",
	        "06ij9xc",
	        [
	            441,
	            141,
	            150
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.dataValue",
	        "0v97vov",
	        [
	            447
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.data",
	        "12tprag",
	        [
	            448
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.query",
	        "0vhj9du",
	        [
	            441,
	            153
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.api",
	        "1plfyj9",
	        [
	            445,
	            446,
	            449,
	            450
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.autocomplete",
	        "0gleizm",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.qtip.styles",
	        "1wmh0f8",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.jquery.qtip",
	        "1pcctjj",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.tooltip.styles",
	        "0fl7wwt",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.tooltip",
	        "0qi5bs5",
	        [
	            454,
	            441,
	            455
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.tooltips",
	        "1s0a024",
	        [
	            442,
	            456
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.autocomplete",
	        "0tb1iv0",
	        [
	            62
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.purge",
	        "05lo0jy",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.ask",
	        "0i04wxd",
	        [
	            442,
	            456
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.browse.styles",
	        "1qfbny7",
	        [],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.browse",
	        "0jn3bf7",
	        [
	            442,
	            101
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.browse.page.autocomplete",
	        "1s0a024",
	        [
	            458,
	            462
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.admin",
	        "1k4tops",
	        [
	            101
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.smw.property",
	        "11eg9sr",
	        [
	            452,
	            153
	        ],
	        "ext.smw"
	    ],
	    [
	        "ext.pageforms.maps",
	        "16q376m"
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
	    "wgServer": "https://wiki.wizard101central.com",
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
	script.src = "/wiki/load.php?debug=true&lang=en&modules=jquery%2Cmediawiki&only=scripts&skin=vector&version=0m39iv0";
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
