/*
MediaWiki:Common.css
*/
/*
* Removes Discussion Tab
*/

#ca-talk { display: none !important; }

/*
* Removes user talk link
*/

#pt-mytalk { display: none; }

/*
* Removes lock icon on HTTPS links
*/

div#content a.external[href ^="https://"], .link-https {
    background: unset;
    padding-right: unset;
}

/*
* Hides admin-only content for regular users
*/

.admin-only {
    display: none;
}

/*
* Modify Toolbox
*/

#t-recentchangeslinked { display: none; }
#t-trackbacklink { display: none; }
#t-print { display: none; }
#t-permalink { display: none; }

/*
* Modify Headertabs
*/

#edittab { display: none; }

/******************************\
**         LIGHT MODE         **
\******************************/
html[data-theme=light] {

/* Site-Owner Identifier */
.mw-userlink[title="User:Jester"],
.mw-userlink[title="User:Olivia"] {
    color: red !important;
    font-weight: bold;
}

/* Infobox Pages */
.infobox-plain-heading {
    color: #544b43;
    font-size: 0.85em;
    font-weight: bold;
    letter-spacing: 0.75px;
    text-transform: uppercase;
}

.data-table {
    background: #fbfbfb;
    border: 0;
    border-top: 1px solid #cd8f52;
    border-collapse: collapse; 
    color: #5a394a; 
    width: 100%;
}


/* Template:BadgeInfobox */
.badge-table {
    background-color: #FBFBFB;
    border-collapse: collapse;
}

.badge-table th:nth-child(1) {
    background-color: rgb(247, 240, 232);
    text-align: center;
}

.badge-table td:nth-child(odd) {
    background-color: rgb(247, 240, 232);
    text-align: center;
}

} /* End light mode */

/******************************\
**         DARK MODE          **
\******************************/
html[data-theme=dark] {

/* Modify TOC display */
#toc, .toc, .mw-warning, .toccolours {
    background-color: #544F4A;
}

/* Modify redirect text color */
#contentSub, #contentSub2 {
    color: #ffffff;
}

/* Page History rules */
#pagehistory li.selected,
.diff .diff-context {
    background-color: #060606; /* Adjust backgrounds on revisions page */
    color: #ffffff;
}

.diff td.diff-deletedline {
    border-color: #DA3A39;
}

.diff td.diff-deletedline .diffchange {
    background: #c94949;
}

.diff td.diff-addedline .diffchange {
    background: #2f689e;
}

/* Browse SMW Properties Pages */
.smwb-datasheet, .smwb-content {
    color: #252525;
}

/* Site-Owner Identifier */
.mw-userlink[title="User:Jester"],
.mw-userlink[title="User:Olivia"] {
    color: #ff3f3f !important;
    font-weight: bold;
}

.data-table {
    background: #545454;
    border-top: 1px solid #cd8f52;
    border: 1px solid #4f4f4f;
    border-collapse: collapse; 
    color: #ffffff; 
    width: 100%;
}

.data-table-subheading {
    background-color: #4a4642 !important;
}

.infobox-plain-heading {
    color: #dbdbdb !important;
    font-size: 0.85em;
    font-weight: bold;
    letter-spacing: 0.75px;
    text-transform: uppercase;
}


/* Template:BadgeInfobox */
.badge-table {
    background-color: #545454;
    border-collapse: collapse;
}

.badge-table th:nth-child(1) {
    background-color: rgb(97, 90, 82);
    text-align: center;
}

.badge-table td:nth-child(odd) {
    background-color: rgb(97, 90, 82);
    text-align: center;
}

} /* End dark mode */


/******************************\
**        GLOBAL RULES        **
\******************************/


/* formatting to blend thumbnails with background for a cleaner look */
.thumb {
     border: none;
     background: transparent;
}

div.thumbinner {
     border: 1px solid #d3b88a;
     border: 1px solid rgba(64, 40, 12, 0.14);
     background: #e3c790;
     background: rgba(146, 95, 0, 0.05);
     box-shadow: none;
     color: #2c2c2c;
     margin: 0 0 10px 0;
     padding: 3px 8px 5px 8px;
}

html .thumbimage {
     border-radius: 4px;
     border: 1px solid #bb9f75;
     background: #dbbc82;
     box-shadow: none;
     color: #2c2c2c;
}

img.thumbborder {
     border: 1px solid #bb9f75;
}

.thumbcaption {
     color: #48sf0c;
}

/* Admin Identifier */
.mw-userlink[title="User:AluraMist"],
.mw-userlink[title="User:Audacioussalix"],
.mw-userlink[title="User:Chariity"],
.mw-userlink[title="User:Dragontamer1016"],
.mw-userlink[title="User:FritzFunBringer"],
.mw-userlink[title="User:Icourt"],
.mw-userlink[title="User:Marcus StrongThief"],
.mw-userlink[title="User:Mayonnaisinator"],
.mw-userlink[title="User:Neth110"],
.mw-userlink[title="User:Potroast42"],
.mw-userlink[title="User:Pyro"],
.mw-userlink[title="User:RedValkyre99"],
.mw-userlink[title="User:VictoriaWildsong"],
.mw-userlink[title="User:Zane"],
.mw-userlink[title="User:Monochromatic Bunny"] {
     color: #ff9600 !important;
     font-weight: bold;
     padding-left: 16px;
     background: url(https://www.wizard101central.com/wiki/images/8/8e/%28Icon%29_WMV.png) center left no-repeat;
     background-size: 15px;
}


/**
 *  Semantic Forms
 */
#sfForm {
    position: relative;
}

/**
 *  Textbox
 */
textarea {
    font-family: Monaco, monospace;
}

/**
 *  Infobox pages
 */
.infobox-hr {
    background: #cd8f52;
}

.infobox-accent-bordertop {
    background: rgba(146, 95, 0, 0.1);
    border-top: 1px solid #cd8f52;
}

/**
 *  Infobox tables
 */

.infobox-table tr {
    vertical-align: top;
}

.infobox-table-partition {
    border-collapse: collapse;
    color: #38332d;
}

.infobox-table-partition tr {
    border-top: 1px solid #c4b08b;
    vertical-align: top;
}

.infobox-table-partition tr:first-child {
    border-top: 0;
}

.infobox-table-partition tr td {
    padding: 6px 9px;
}

.infobox-table-partition tr td:first-child {
    padding: 6px 0 6px 9px;
}

/**
 *  Data tables
 */

table .data-table {
    border: 0;  /* override border-top */
}

.data-table tr {
    border-top: 1px solid #eae6d6;
    vertical-align: top;
}

.data-table tr td {
    border-left: 1px solid #eae6d6;
}

.data-table.petinfobox tr td {
    border-left: none;
}

.tccardpackvariation tr {
    display: flex;
    flex-wrap: wrap;
}

.data-table.tccardpackvariation td {
    flex: auto;
    display: block;
    border: none;
}

.data-table.tcenchantmentvariation td {
    border: none;
}

.data-table.tcenchantmentvariation tr {
    border: none;
}

tr.spaceover>td {
    padding-top: 9px;
}

tr.spaceunder>td {
    padding-bottom: 9px;
}

.data-table-heading {
    background: #5A394A; 
    border-bottom: 2px solid #d6c06b; 
    color: #fffcde; 
    font-weight: bold;
}

.data-table-subheading {
    background: #f3f1ec;
}

.data-table-heading .mw-collapsible-toggle a {
    color: #fffcde;
}

.data-table-faint {
    color: #9c8a92;
}

/**
 *  Data table - yellow
 */
 
.data-table-yellow {
    background: #ffffcc;
    color: #5a394a;
}

/**
 *  Data table - green
 */
 
.data-table-green {
    background: #cff1e2;
    color: #5a394a;
}

.data-table-green tr, tr.data-table-green, tr.data-table-green + tr {
    border-top: 1px solid #b7dcd8;
    vertical-align: top;
}

.data-table-green tr td, tr.data-table-green td, td.data-table-green {
    border-left: 1px solid #b7dcd8;
}

/**
 *  Data table - purple
 */
 
.data-table-purple {
    background: #e4cae4;
    color: #5a394a;
}

.data-table-purple tr, tr.data-table-purple, tr.data-table-purple + tr {
    border-top: 1px solid #d8bfd8;
    vertical-align: top;
}

.data-table-purple tr td, tr.data-table-purple td, td.data-table-purple {
    border-left: 1px solid #d8bfd8;
}

/**
 *  Data tables - normalizing
 */

.data-table tr:first-child {
    border-top: 0;
}
.data-table tr td:first-child {
    border-left: 0;
}

/**
 *  Documentation pages
 */
.doc-heading {
    border-top: 1px solid #cd8f52; 
    font-size: 1.4em; 
    margin-top: 18px; 
    padding: 12px 0;
}

.doc-box {
    background: rgba(146, 95, 0, 0.1);
    border: 1px solid #cd8f52;
    padding: 6px;
}

.doc-table {
    background: rgba(146, 95, 0, 0.1); 
    border: 1px solid #cd8f52; 
    border-collapse: collapse;
    width: 100%;
}

.doc-table tr {
    vertical-align: top;
}

.doc-table td {
    padding: 3px;
}

/**
 *  UI elements
 */
 
.ui-gold-button {
    background: #d6c06b !important;
    font-size: 1.1em;
    color: #5a394a !important;
    letter-spacing: 1px;
    border: 0 !important;
    font-family: Times, serif;
    font-weight: bold;
    padding: 9px 24px !important;
}

.ui-gold-wrapper {
    display: inline-block;
    border: 1px solid #d6c06b;
    padding: 1px;
}

/* Tool tip customization */
.wiki-tooltip {
  background: #444;
  border-radius: 3px;
  display: none;
  color: #eee;
  padding: 3px 9px;
  position: absolute;
  z-index: 1;
}

.wiki-tooltip a {
  color: #719feb;
}

.help {
  display: inline-block;
}

.help a {
    cursor: help;
}

.help:hover .wiki-tooltip {
  display: block;
}

/* Main Page CSS */

.fpbox {
     border-radius: 4px;
     border: 1px solid #d3b88a;
     border: 1px solid rgba(64, 40, 12, 0.14);
     background: #e3c790;
     background: rgba(146, 95, 0, 0.09);
     color: #2c2c2c;
     margin: 0 10px 10px 10px;
     padding: 8px;
}

.fpbox:hover {
     background: rgba(146, 95, 0, 0.11);
}

.fpmbox {
     border-radius: 4px;
     border: 2px solid #bb9f75;
     border: 2px solid rgba(64, 40, 12, 0.20);
     background: #e3c790;
     background: rgba(146, 95, 0, 0.07);
     color: #2c2c2c;
     margin: 0 10px 10px 10px;
     padding: 8px;
}

.fpmbox:hover {
     background: rgba(146, 95, 0, 0.11);
}

.heading {
     border-bottom: 1px solid #2c2c2c;
     font-family: WizardRegular;
     font-size: 135%;
     font-weight: bold;
     padding: 0 0 5px 0;
}

.subheading {
     margin: 0 0 0 0;
     padding: 0 0 10px 0;
}

/* Template CSS */
.noresults {
    color: grey;
}

div.hatnote {
    font-style: italic;
    margin-top: 0.2em;
    padding-left: 1.6em;
}

.questlegendstat {
    font-weight: bold;
    text-transform: uppercase;
}

/* Template:BadgeInfobox */
.badge-table-heading {
    border-bottom: 5px solid rgb(205, 143, 82);
    font-family: sans-serif;
    padding: 7px;
}

.badge-table tr {
    border-bottom: 2px solid rgb(245, 222, 179);
}

.badge-table td:nth-child(even) {
    padding: 10px;
}

/* Template:PackInfobox + Template:FormatDropLinks */
.drop-tag {
    display: inline;
    padding-left: 5px;
    font-size: 0.85em;
}

.drop-tag:hover .wiki-tooltip {
    display: block;
}

@import url('https://fonts.googleapis.com/css?family=Lato');/*
MediaWiki:Vector.css
*/
/* CSS placed here will affect users of the Vector skin */
/* keep nested list fonts from continually decreasing in size with each nesting */
#mw-panel div.portal div.body ul li {
        font-size: small !important;
}

/* Allow popup submenus to overflow the sidebar area */
#mw-panel div.portal div.body ul li {
        overflow: visible !important;
}

/*
* Removes Navigation portion of sidebar
*/

#p-Navigation {display: none !important; }


/* minor adjustments to the sidebar area for the Vector skin */
.menuSidebar ul div { 
        top: -1px !important; /* vertical offset of submenus */
}

.menuSidebar ul {
 width: 8em; /* width of main menu */
}