function isCompatible(){if(navigator.appVersion.indexOf('MSIE')!==-1&&parseFloat(navigator.appVersion.split('MSIE')[1])<6){return false;}return true;}var startUp=function(){mw.config=new mw.Map(true);mw.loader.addSource({"local":{"loadScript":"/wiki/load.php","apiScript":"/wiki/api.php"}});mw.loader.register([["site","1693090222",[],"site"],["noscript","1693090222",[],"noscript"],["startup","1693635764",[],"startup"],["filepage","1693090222"],["user.groups","1693090222",[],"user"],["user","1693090222",[],"user"],["user.cssprefs","1693635764",["mediawiki.user"],"private"],["user.options","1693635764",[],"private"],["user.tokens","1693090222",[],"private"],["mediawiki.language.data","1693090222",["mediawiki.language.init"]],["skins.chick","1693090222"],["skins.cologneblue","1693090222"],["skins.modern","1693090222"],["skins.monobook","1693090222"],["skins.nostalgia","1693090222"],["skins.simple","1693090222"],["skins.standard","1693090222"],["skins.vector","1693090222"],["jquery",
"1693090222"],["jquery.appear","1693090222"],["jquery.arrowSteps","1693090222"],["jquery.async","1693090222"],["jquery.autoEllipsis","1693090222",["jquery.highlightText"]],["jquery.badge","1693090222"],["jquery.byteLength","1693090222"],["jquery.byteLimit","1693090222",["jquery.byteLength"]],["jquery.checkboxShiftClick","1693090222"],["jquery.client","1693090222"],["jquery.collapsibleTabs","1693090222"],["jquery.color","1693090222",["jquery.colorUtil"]],["jquery.colorUtil","1693090222"],["jquery.cookie","1693090222"],["jquery.delayedBind","1693090222"],["jquery.expandableField","1693090222",["jquery.delayedBind"]],["jquery.farbtastic","1693090222",["jquery.colorUtil"]],["jquery.footHovzer","1693090222"],["jquery.form","1693090222"],["jquery.getAttrs","1693090222"],["jquery.highlightText","1693090222",["jquery.mwExtension"]],["jquery.hoverIntent","1693090222"],["jquery.json","1693090222"],["jquery.localize","1693090222"],["jquery.makeCollapsible","1693090232"],["jquery.mockjax",
"1693090222"],["jquery.mw-jump","1693090222"],["jquery.mwExtension","1693090222"],["jquery.placeholder","1693090222"],["jquery.qunit","1693090222"],["jquery.qunit.completenessTest","1693090222",["jquery.qunit"]],["jquery.spinner","1693090222"],["jquery.jStorage","1693090222",["jquery.json"]],["jquery.suggestions","1693090222",["jquery.autoEllipsis"]],["jquery.tabIndex","1693090222"],["jquery.tablesorter","1693090291",["jquery.mwExtension"]],["jquery.textSelection","1693090222",["jquery.client"]],["jquery.validate","1693090222"],["jquery.xmldom","1693090222"],["jquery.tipsy","1693090222"],["jquery.ui.core","1693090222",["jquery"],"jquery.ui"],["jquery.ui.widget","1693090222",[],"jquery.ui"],["jquery.ui.mouse","1693090222",["jquery.ui.widget"],"jquery.ui"],["jquery.ui.position","1693090222",[],"jquery.ui"],["jquery.ui.draggable","1693090222",["jquery.ui.core","jquery.ui.mouse","jquery.ui.widget"],"jquery.ui"],["jquery.ui.droppable","1693090222",["jquery.ui.core","jquery.ui.mouse",
"jquery.ui.widget","jquery.ui.draggable"],"jquery.ui"],["jquery.ui.resizable","1693090222",["jquery.ui.core","jquery.ui.widget","jquery.ui.mouse"],"jquery.ui"],["jquery.ui.selectable","1693090222",["jquery.ui.core","jquery.ui.widget","jquery.ui.mouse"],"jquery.ui"],["jquery.ui.sortable","1693090222",["jquery.ui.core","jquery.ui.widget","jquery.ui.mouse"],"jquery.ui"],["jquery.ui.accordion","1693090222",["jquery.ui.core","jquery.ui.widget"],"jquery.ui"],["jquery.ui.autocomplete","1693090222",["jquery.ui.core","jquery.ui.widget","jquery.ui.position"],"jquery.ui"],["jquery.ui.button","1693090222",["jquery.ui.core","jquery.ui.widget"],"jquery.ui"],["jquery.ui.datepicker","1693090222",["jquery.ui.core"],"jquery.ui"],["jquery.ui.dialog","1693090222",["jquery.ui.core","jquery.ui.widget","jquery.ui.button","jquery.ui.draggable","jquery.ui.mouse","jquery.ui.position","jquery.ui.resizable"],"jquery.ui"],["jquery.ui.progressbar","1693090222",["jquery.ui.core","jquery.ui.widget"],"jquery.ui"],[
"jquery.ui.slider","1693090222",["jquery.ui.core","jquery.ui.widget","jquery.ui.mouse"],"jquery.ui"],["jquery.ui.tabs","1693090222",["jquery.ui.core","jquery.ui.widget"],"jquery.ui"],["jquery.effects.core","1693090222",["jquery"],"jquery.ui"],["jquery.effects.blind","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.bounce","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.clip","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.drop","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.explode","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.fade","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.fold","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.highlight","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.pulsate","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.scale","1693090222",["jquery.effects.core"],"jquery.ui"],[
"jquery.effects.shake","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.slide","1693090222",["jquery.effects.core"],"jquery.ui"],["jquery.effects.transfer","1693090222",["jquery.effects.core"],"jquery.ui"],["mediawiki","1693090222"],["mediawiki.api","1693090222",["mediawiki.util"]],["mediawiki.api.category","1693090222",["mediawiki.api","mediawiki.Title"]],["mediawiki.api.edit","1693090222",["mediawiki.api","mediawiki.Title"]],["mediawiki.api.parse","1693090222",["mediawiki.api"]],["mediawiki.api.titleblacklist","1693090222",["mediawiki.api","mediawiki.Title"]],["mediawiki.api.watch","1693090222",["mediawiki.api","user.tokens"]],["mediawiki.debug","1693090222",["jquery.footHovzer"]],["mediawiki.debug.init","1693090222",["mediawiki.debug"]],["mediawiki.feedback","1693090222",["mediawiki.api.edit","mediawiki.Title","mediawiki.jqueryMsg","jquery.ui.dialog"]],["mediawiki.htmlform","1693090222"],["mediawiki.notification","1693090222",["mediawiki.page.startup"]],[
"mediawiki.notify","1693090222"],["mediawiki.searchSuggest","1693090232",["jquery.autoEllipsis","jquery.client","jquery.placeholder","jquery.suggestions"]],["mediawiki.Title","1693090222",["mediawiki.util"]],["mediawiki.Uri","1693090222"],["mediawiki.user","1693090222",["jquery.cookie","mediawiki.api"]],["mediawiki.util","1693090231",["jquery.client","jquery.cookie","jquery.mwExtension","mediawiki.notify"]],["mediawiki.action.edit","1693090222",["jquery.textSelection","jquery.byteLimit"]],["mediawiki.action.edit.preview","1693090222",["jquery.form","jquery.spinner"]],["mediawiki.action.history","1693090222",[],"mediawiki.action.history"],["mediawiki.action.history.diff","1693090222",[],"mediawiki.action.history"],["mediawiki.action.view.dblClickEdit","1693090222",["mediawiki.util"]],["mediawiki.action.view.metadata","1693090232"],["mediawiki.action.view.rightClickEdit","1693090222"],["mediawiki.action.watch.ajax","1693090222",["mediawiki.page.watch.ajax"]],["mediawiki.language",
"1693090222",["mediawiki.language.data","mediawiki.cldr"]],["mediawiki.cldr","1693090222",["mediawiki.libs.pluralruleparser"]],["mediawiki.libs.pluralruleparser","1693090222"],["mediawiki.language.init","1693090222"],["mediawiki.jqueryMsg","1693090222",["mediawiki.util","mediawiki.language"]],["mediawiki.libs.jpegmeta","1693090222"],["mediawiki.page.ready","1693090222",["jquery.checkboxShiftClick","jquery.makeCollapsible","jquery.placeholder","jquery.mw-jump","mediawiki.util"]],["mediawiki.page.startup","1693090222",["jquery.client","mediawiki.util"]],["mediawiki.page.watch.ajax","1693090249",["mediawiki.page.startup","mediawiki.api.watch","mediawiki.util","mediawiki.notify","jquery.mwExtension"]],["mediawiki.special","1693090222"],["mediawiki.special.block","1693090222",["mediawiki.util"]],["mediawiki.special.changeemail","1693090222",["mediawiki.util"]],["mediawiki.special.changeslist","1693090222",["jquery.makeCollapsible"]],["mediawiki.special.movePage","1693090222",[
"jquery.byteLimit"]],["mediawiki.special.preferences","1693090222"],["mediawiki.special.recentchanges","1693090222",["mediawiki.special"]],["mediawiki.special.search","1693092700"],["mediawiki.special.undelete","1693090222"],["mediawiki.special.upload","1693090419",["mediawiki.libs.jpegmeta","mediawiki.util"]],["mediawiki.special.javaScriptTest","1693090222",["jquery.qunit"]],["mediawiki.tests.qunit.testrunner","1693090222",["jquery.qunit","jquery.qunit.completenessTest","mediawiki.page.startup","mediawiki.page.ready"]],["mediawiki.legacy.ajax","1693090222",["mediawiki.util","mediawiki.legacy.wikibits"]],["mediawiki.legacy.commonPrint","1693090222"],["mediawiki.legacy.config","1693090222",["mediawiki.legacy.wikibits"]],["mediawiki.legacy.IEFixes","1693090222",["mediawiki.legacy.wikibits"]],["mediawiki.legacy.protect","1693090222",["mediawiki.legacy.wikibits","jquery.byteLimit"]],["mediawiki.legacy.shared","1693090222"],["mediawiki.legacy.oldshared","1693090222"],[
"mediawiki.legacy.upload","1693090222",["mediawiki.legacy.wikibits","mediawiki.util"]],["mediawiki.legacy.wikibits","1693090222",["mediawiki.util"]],["mediawiki.legacy.wikiprintable","1693090222"],["ext.smw","1693090222",[],"ext.smw"],["ext.smw.style","1693090222",[],"ext.smw"],["ext.smw.tooltips","1693090222",["mediawiki.legacy.wikibits","ext.smw.style"],"ext.smw"],["ext.srf.jqplot","1693090222"],["ext.srf.jqplotbar","1693090222",["ext.srf.jqplot"]],["ext.srf.jqplotpointlabels","1693090222",["ext.srf.jqplotbar"]],["ext.srf.jqplotpie","1693090222",["ext.srf.jqplot"]],["ext.srf.timeline","1693090222",["mediawiki.legacy.wikibits"]],["ext.srf.d3core","1693090222"],["ext.srf.d3treemap","1693090222",["ext.srf.d3core"]],["jquery.progressbar","1693090222"],["ext.srf.jit","1693090222"],["ext.srf.jitgraph","1693090222",["mediawiki.legacy.wikibits","jquery.progressbar","ext.srf.jit"]],["ext.srf.jcarousel","1693090222"],["ext.srf.filtered","1693090222"],["ext.srf.filtered.list-view","1693090222",
["ext.srf.filtered"]],["ext.srf.filtered.value-filter","1693090222",["ext.srf.filtered"]],["ext.semanticforms.main","1693090222",["jquery.ui.core","jquery.ui.autocomplete","jquery.ui.button","jquery.ui.sortable","jquery.ui.widget","ext.semanticforms.fancybox","ext.semanticforms.autogrow"]],["ext.semanticforms.fancybox","1693090222"],["ext.semanticforms.autogrow","1693090222"],["ext.semanticforms.popupformedit","1693090222",["jquery"]],["ext.semanticforms.autoedit","1693090222",["jquery"]],["ext.semanticforms.submit","1693090222",["jquery"]],["ext.semanticforms.collapsible","1693090222",["jquery"]],["ext.semanticforms.wikieditor","1693090222",["ext.semanticforms.main","jquery.wikiEditor"]],["ext.semanticforms.imagepreview","1693090222"],["sii.image","1693090222"],["ext.pageschemas.main","1693090222",["jquery"]],["ext.pageschemas.generatepages","1693090222",["jquery"]],["ext.categoryTree","1693090246"],["ext.categoryTree.css","1693090222"]]);mw.config.set({"wgLoadScript":"/wiki/load.php"
,"debug":false,"skin":"vector","stylepath":"/wiki/skins","wgUrlProtocols":"http\\:\\/\\/|https\\:\\/\\/|ftp\\:\\/\\/|irc\\:\\/\\/|ircs\\:\\/\\/|gopher\\:\\/\\/|telnet\\:\\/\\/|nntp\\:\\/\\/|worldwind\\:\\/\\/|mailto\\:|news\\:|svn\\:\\/\\/|git\\:\\/\\/|mms\\:\\/\\/|\\/\\/","wgArticlePath":"/wiki/$1","wgScriptPath":"/wiki","wgScriptExtension":".php","wgScript":"/wiki/index.php","wgVariantArticlePath":false,"wgActionPaths":{},"wgServer":"//www.wizard101central.com","wgUserLanguage":"en","wgContentLanguage":"en","wgVersion":"1.20.0","wgEnableAPI":true,"wgEnableWriteAPI":true,"wgMainPageTitle":"Wizard101 Wiki","wgFormattedNamespaces":{"-2":"Media","-1":"Special","0":"","1":"Talk","2":"User","3":"User talk","4":"Wizard101 Wiki","5":"Wizard101 Wiki talk","6":"File","7":"File talk","8":"MediaWiki","9":"MediaWiki talk","10":"Template","11":"Template talk","12":"Help","13":"Help talk","14":"Category","15":"Category talk","100":"Creature","102":"Spell","104":"Pet","106":"Location","108":"NPC",
"110":"Quest","112":"Item","114":"Minion","116":"TreasureCard","118":"ItemCard","120":"Reagent","122":"Snack","124":"PetAbility","128":"Mount","130":"House","132":"Basic","134":"Polymorph","136":"Contest","138":"Fish","140":"LockedChest","142":"Jewel","144":"Recipe","146":"BeastmoonForm","148":"Set","152":"Property","153":"Property talk","156":"Form","157":"Form talk","158":"Concept","159":"Concept talk","274":"Widget","275":"Widget talk"},"wgNamespaceIds":{"media":-2,"special":-1,"":0,"talk":1,"user":2,"user_talk":3,"wizard101_wiki":4,"wizard101_wiki_talk":5,"file":6,"file_talk":7,"mediawiki":8,"mediawiki_talk":9,"template":10,"template_talk":11,"help":12,"help_talk":13,"category":14,"category_talk":15,"creature":100,"spell":102,"pet":104,"location":106,"npc":108,"quest":110,"item":112,"minion":114,"treasurecard":116,"itemcard":118,"reagent":120,"snack":122,"petability":124,"mount":128,"house":130,"basic":132,"polymorph":134,"contest":136,"fish":138,"lockedchest":140,"jewel":142,
"recipe":144,"beastmoonform":146,"set":148,"property":152,"property_talk":153,"form":156,"form_talk":157,"concept":158,"concept_talk":159,"widget":274,"widget_talk":275,"image":6,"image_talk":7,"project":4,"project_talk":5},"wgSiteName":"Wizard101 Wiki","wgFileExtensions":["png","gif"],"wgDBname":"wikidb","wgFileCanRotate":true,"wgAvailableSkins":{"myskin":"MySkin","modern":"Modern","cologneblue":"CologneBlue","nostalgia":"Nostalgia","standard":"Standard","simple":"Simple","vector":"Vector","monobook":"MonoBook","wptouch":"WPtouch","chick":"Chick"},"wgExtensionAssetsPath":"/wiki/extensions","wgCookiePrefix":"wikidb_mw_","wgResourceLoaderMaxQueryLength":-1,"wgCaseSensitiveNamespaces":[]});};if(isCompatible()){document.write("\x3cscript src=\"/wiki/load.php?debug=false\x26amp;lang=en\x26amp;modules=jquery%2Cmediawiki\x26amp;only=scripts\x26amp;skin=vector\x26amp;version=20121106T212624Z\"\x3e\x3c/script\x3e");}delete isCompatible;
/* cache key: wikidb-mw_:resourceloader:filter:minify-js:7:42254643261cfa152f2c4405c6978c43 */