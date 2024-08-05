/*
MediaWiki:Common.css
*/
/*
** Import statements
*/
@import url(https://fonts.googleapis.com/css?family=Lato);

/*
** Removes Discussion Tab
*/
#ca-talk {
    display: none !important;
}

/*
** Removes user talk link
*/
#pt-mytalk {
    display: none !important;
}

/*
** Adjust search bar
*/
div#p-search {
    float: none;
    overflow: hidden;
    margin: auto 9px;
}

/*
** Removes lock icon on HTTPS links
*/
div#content a.external[href ^="https://"], .link-https {
    background: unset;
    padding-right: unset;
}

/*
** Hides admin-only content for regular users
*/
.admin-only {
    display: none;
}

/*
** Modify Sidebar
*/
#p-Staff_Resources {
    display: none; /* Hide staff links from regular users */
}

#mw-panel.collapsible-nav .portal h3,
#mw-panel.collapsible-nav .portal h3 a {
    color: #f5db77 !important;
}

#mw-panel.collapsible-nav .portal h3:hover,
#mw-panel.collapsible-nav .portal h3 a:hover {
    color: #f5db77 !important;
    text-decoration: underline;
}

/* Mobile Sidebar */
.csidebarcontent h3 {
    margin-left: 9px;
}

/*
** Modify Toolbox
*/
#t-recentchangeslinked { display: none; }
#t-trackbacklink { display: none; }
#t-print { display: none; }
#t-permalink { display: none; }

/*
** Modify Headertabs
*/
#edittab {
    display: none;
}

/*
** Modify how text-overflow is handled
*/
pre {
    overflow-wrap: break-word;
    word-break: break-word;
}


/******************************\
**         LIGHT MODE         **
\******************************/


html[data-theme=light] ::selection {
    background-color: #3367d1;
    color: #ffffff;
}

/*
** Vector link colors
*/
html[data-theme=light] #mw-navigation a, 
html[data-theme=light] #mw-panel a, 
html[data-theme=light] #preftoc a, 
html[data-theme=light] #footer a {
    color: #955516!important;
}

html[data-theme=light] .mw-body a.external {
    color: #955516;
}

html[data-theme=light] .mw-body a:visited {
    color: #ad8461;
}

html[data-theme=light] .mw-body a.external:visited {
    color: #ad8461;
}

html[data-theme=light] .new {
    color: #ba0000;
}

html[data-theme=light] .new:visited {
    color: #a55858 !important;
}

/* Special:Ask */
html[data-theme=light] table.smw-ask-otheroptions td {
    background-color: #dbdbdb;
    border: 1px solid #dbdbdb;
    padding: 9px;
}

html[data-theme=light] table.smw-ask-otheroptions {
    text-align: center;
}

html[data-theme=light] table.smw-ask-otheroptions td {
    background-color: #dbdbdb;
    border: 1px solid #4f4f4f;
    padding: 9px;
}

html[data-theme=light] table.smw-ask-otheroptions td:nth-child(odd) {
    color: #544b43;
    font-size: 0.85em;
    font-weight: bold;
    letter-spacing: 0.75px;
    text-transform: uppercase;
}

html[data-theme=light] div.autocomplete-suggestions {
    background-color: #ffffff;
}

html[data-theme=light] div.autocomplete-selected {
    background-color: #f0f0f0;
}

html[data-theme=light] a.smw-ask-action-btn,
html[data-theme=light] a.smw-ask-action-btn:visited {
    color: #fff;
}

/* Site-Owner Identifier */
html[data-theme=light] .mw-userlink[title="User:Jester"],
html[data-theme=light] .mw-userlink[title="User:Olivia"] {
    color: red !important;
    font-weight: bold;
}

/*
** Containers
*/
[data-theme=light] .container-bg {
    background-color: #fbfbfb;
    border: 1px solid #dbdbdb;
}

/*
** Data tables
*/
html[data-theme=light] .data-table {
    background: #fbfbfb;
    border: 1px solid #dbdbdb;
    border-top: 1px solid #cd8f52;
    color: #5a394a;
}

html[data-theme=light] .data-table-subheading {
    background: #f3f1ec;
}

html[data-theme=light] .data-table tr {
    border-top: 1px solid #eae6d6;
    vertical-align: top;
}

html[data-theme=light] .data-table tr td {
    border-left: 1px solid #eae6d6;
}

/*
** Data table - purple
*/
html[data-theme=light] .data-table-purple {
    background: #e4cae4;
    color: #5a394a;
}

html[data-theme=light] .data-table-purple tr, 
html[data-theme=light] tr.data-table-purple, 
html[data-theme=light] tr.data-table-purple + tr {
    border-top: 1px solid #d8bfd8;
    vertical-align: top;
}

html[data-theme=light] .data-table-purple tr td, 
html[data-theme=light] tr.data-table-purple td, 
html[data-theme=light] td.data-table-purple {
    border-left: 1px solid #d8bfd8;
}

/*
** Data table - green
*/
html[data-theme=light] .data-table-green {
    background: #cff1e2;
    color: #5a394a;
}

html[data-theme=light] .data-table-green tr, 
html[data-theme=light] tr.data-table-green, 
html[data-theme=light] tr.data-table-green + tr {
    border-top: 1px solid #b7dcd8;
    vertical-align: top;
}

html[data-theme=light] .data-table-green tr td, 
html[data-theme=light] tr.data-table-green td, 
html[data-theme=light] td.data-table-green {
    border-left: 1px solid #b7dcd8;
}

/*
**  Data table - yellow
*/
html[data-theme=light] .data-table-yellow {
    background: #ffffcc;
    color: #5a394a;
}


/*
** Infobox Pages
*/
html[data-theme=light] .infobox {
    background: #fbfbfb;
    border: 1px solid #eae6d6;
    color: #5a394a;
}

html[data-theme=light] .infobox-header {
    background-color: #f3f1ec;
}

html[data-theme=light] .infobox tr td {
    border: 1px solid #eae6d6;
}

html[data-theme=light] .infobox-table {
    background-color: #fbfbfb;
    color: #5a394a;
}

html[data-theme=light] .infobox-table tr {
    border-top: 1px solid #eae6d6;
}

html[data-theme=light] .container-purple {
    background: #e4cae4;
    color: #5a394a;
    border: 1px solid #dbdbdb;
}

html[data-theme=light] .container-green {
    background: #cff1e2;
    color: #5a394a;
    border: 1px solid #dbdbdb;
}

html[data-theme=light] .container-yellow {
    background: #ffffcc;
    color: #5a394a;
    border: 1px solid #dbdbdb;
}

html[data-theme=light] .infobox-plain-heading {
    color: #544b43;
    font-size: 0.85em;
    font-weight: bold;
    letter-spacing: 0.75px;
    text-transform: uppercase;
}

/* RDF Feed on Page Preview */
html[data-theme=light] #bodyContent span.swmfactboxheadbrowse a {
    color: #955516;
}

html[data-theme=light] #bodyContent span.swmfactboxheadbrowse a:hover {
    color: #955516;
    text-decoration: underline;
}

/*
** Template:Acquisition Sources
*/
html[data-theme=light] .columns {
    column-rule: 1px solid #eae6d6;
}

html[data-theme=light] .column-category {
    border-top: 1px solid #eae6d6;
}

/*
** Template:BadgeInfobox
*/
html[data-theme=light] .badge-table {
    background-color: #FBFBFB;
    border-collapse: collapse;
}

html[data-theme=light] .badge-table th:nth-child(1) {
    background-color: rgb(247, 240, 232);
    text-align: center;
}

html[data-theme=light] .badge-table td:nth-child(odd) {
    background-color: rgb(247, 240, 232);
    text-align: center;
}

/* End light mode */

/******************************\
**         DARK MODE          **
\******************************/

html[data-theme=dark] ::selection {
    background-color: #063ba5;
    color: #ffffff;
}

html[data-theme=dark] .searchButton {
    background-color: #000000 !important;
}

/*
** Table of Contents display
*/
html[data-theme=dark] #toc, 
html[data-theme=dark] .toc, 
html[data-theme=dark] .mw-warning, 
html[data-theme=dark] .toccolours {
    background-color: #544F4A;
}

/*
** Update text color
*/
html[data-theme=dark] #contentSub, 
html[data-theme=dark] #contentSub2 {
    color: #ffffff;
}

/*
** Vector link colors
*/
html[data-theme=dark] #mw-navigation a, 
html[data-theme=dark] #mw-panel a, 
html[data-theme=dark] #preftoc a, #footer a {
    color: #cfaf53!important;
}

html[data-theme=dark] .mw-body a.external {
    color: #cfaf53;
}

html[data-theme=dark] .mw-body a:visited {
    color: #A78A34;
}

html[data-theme=dark] .mw-body a.external:visited {
    color: #A78A34;
}

html[data-theme=dark] .mw-plusminus-neg {
    color: #ff3f3f;
}

html[data-theme=dark] .mw-notification, 
html[data-theme=dark] .mw-notification-content {
    color: #ffffff;
    background-color: #5d5751;
}

html[data-theme=dark] .new {
    color: #ff3f3f;
}

html[data-theme=dark] .new:visited {
    color: #ce2727!important;
}

html[data-theme=dark] .wikitable th, 
html[data-theme=dark] .mw_metadata th, 
html[data-theme=dark] .mw_metadata td, 
html[data-theme=dark] #filetoc {
    background-color: #4a4642;
}

html[data-theme=dark] .thumbcaption {
    color: #ffffff;
}

/* Dropdown selector color loading fix */
html[data-theme=dark] .oo-ui-dropdownWidget.oo-ui-widget-enabled .oo-ui-dropdownWidget-handle,
html[data-theme=dark] .oo-ui-dropdownInputWidget select {
    background-color: #3e3c3c;
    color: #ffffff!important;
}

/* Special:Ask */
html[data-theme=dark] table.smw-ask-otheroptions td {
    background-color: #f3f1ec;
    border: 1px solid #4f4f4f;
    padding: 9px;
}

html[data-theme=dark] table.smw-ask-otheroptions {
    text-align: center;
}

html[data-theme=dark] table.smw-ask-otheroptions td {
    background-color: #4a4642;
    border: 1px solid #4f4f4f;
    padding: 9px;
}

html[data-theme=dark] table.smw-ask-otheroptions td:nth-child(odd) {
    color: #ffffff;
    font-size: 0.85em;
    font-weight: bold;
    letter-spacing: 0.75px;
    text-transform: uppercase;
}

html[data-theme=dark] div.autocomplete-suggestions {
    background-color: #000000;
}

html[data-theme=dark] div.autocomplete-selected {
    background-color: #0f0f0f;
}

html[data-theme=dark] a.smw-ask-action-btn,
html[data-theme=dark] a.smw-ask-action-btn:visited {
    color: #fff;
}

html[data-theme=dark] .smw-callout-info {
    border: 1px solid #1b809e;
    background-color: #1b809e;
    border-left-width: 5px;
    border-left-color: #14414f;
}

html[data-theme=dark] .smw-callout-error {
    border: 1px solid #ce4844;
    background-color: #ce4844;
    border-left-width: 5px;
    border-left-color: #7d2927;
}

/* Special:FileList */
html[data-theme=dark] .mw-datatable th {
    background-color: #4a4642;
}

html[data-theme=dark] .mw-datatable td {
    background-color: #545454;
}

html[data-theme=dark] .mw-datatable tr:hover td {
    background-color: #54545e;
}

html[data-theme=dark] .mw-datatable {
    color: #ffffff;
}

/* Special:Browse */
html[data-theme=dark] .smwb-factbox {
    border-left: 0.5em solid #4a4642;
    color: #ffffff;
}

html[data-theme=dark] .smwb-title {
    background-color: #4a4642;
}

html[data-theme=dark] .smwb-propvalue .smwb-prophead {
    background-color: #4a4642;
}

html[data-theme=dark] .smwb-propvalue .smwb-propval {
    background-color: #545454;
}

html[data-theme=dark] .smwb-center {
    background-color: #4a4642;
}

html[data-theme=dark] .smwb-ipropvalue .smwb-propval {
    background-color: #545454;
}

html[data-theme=dark] .smwb-ipropvalue .smwb-prophead {
    background-color: #4a4642;
}

html[data-theme=dark] .smwb-ifactbox {
    border-right: 0.5em solid #4a4642;
}

html[data-theme=dark] .smwb-cell {
    border-top: 2px solid #4f4f4f;
}

html[data-theme=dark] .smwb-bottom {
    border-bottom: 2px solid #4f4f4f;
}

/* RDF Feed on Page Preview */
html[data-theme=dark] div.smwfact {
    background-color: #4a4642; 
    border: 1px solid #666;
}

html[data-theme=dark] div.smwfact td, html[data-theme=dark] div.smwfact tr, html[data-theme=dark] div.smwfact table {
    background-color: #4f4f4f;
}

html[data-theme=dark] table.smwfacttable {
    border-top: 1px dotted #545454;
}

html[data-theme=dark] .smwfact tbody > tr.row-even > td {
    background-color: #545454;
    color: #ffffff;
}

html[data-theme=dark] #bodyContent span.swmfactboxheadbrowse a {
    color: #cfaf53;
}

html[data-theme=dark] #bodyContent span.swmfactboxheadbrowse a:hover {
    color: #cfaf53;
    text-decoration: underline;
}

/*
** Page History
*/
html[data-theme=dark] #pagehistory li.selected,
html[data-theme=dark] .diff .diff-context {
    background-color: #060606; /* Adjust backgrounds on revisions page */
    color: #ffffff;
}

html[data-theme=dark] .diff td.diff-deletedline {
    border-color: #DA3A39;
}

html[data-theme=dark] .diff td.diff-deletedline .diffchange {
    background: #c94949;
}

html[data-theme=dark] .diff td.diff-addedline .diffchange {
    background: #2f689e;
}

/*
** Browse SMW Properties Pages
*/
html[data-theme=dark] .smwb-datasheet, 
html[data-theme=dark] .smwb-content {
    color: #252525;
}

/*
** Site-Owner Identifier
*/
html[data-theme=dark] .mw-userlink[title="User:Jester"],
html[data-theme=dark] .mw-userlink[title="User:Olivia"] {
    color: #ff3f3f !important;
    font-weight: bold;
}

/*
** Data tables
*/
html[data-theme=dark] .data-table {
    background: #545454;
    border-top: 1px solid #cd8f52;
    border: 1px solid #4f4f4f;
    color: #ffffff;
}

html[data-theme=dark] .data-table-subheading {
    background-color: #4a4642;
}

html[data-theme=dark] .data-table tr {
    border-top: 1px solid #424242;
    vertical-align: top;
}

html[data-theme=dark] .data-table tr td {
    border-left: 1px solid #424242;
}

/*
** Containers
*/
[data-theme=dark] .container-bg {
    background-color: #545454;
    border: 1px solid #4f4f4f;
}

/*
** Data table - purple
*/

html[data-theme=dark] .data-table-purple {
    background: #765182;
    color: #ffffff;
}

html[data-theme=dark] .data-table-purple tr, 
html[data-theme=dark] tr.data-table-purple, 
html[data-theme=dark] tr.data-table-purple + tr {
    border-top: 1px solid #654670;
    vertical-align: top;
}

html[data-theme=dark] .data-table-purple tr td, 
html[data-theme=dark] tr.data-table-purple td, 
html[data-theme=dark] td.data-table-purple {
    border-left: 1px solid #654670;
}

/*
** Data table - green
*/

html[data-theme=dark] .data-table-green {
    background: #536746;
    color: #ffffff;
}

html[data-theme=dark] .data-table-green tr, 
html[data-theme=dark] tr.data-table-green, 
html[data-theme=dark] tr.data-table-green + tr {
    border-top: 1px solid #435439;
    vertical-align: top;
}

html[data-theme=dark] .data-table-green tr td, 
html[data-theme=dark] tr.data-table-green td, 
html[data-theme=dark] td.data-table-green {
    border-left: 1px solid #435439;
}

/*
** Data table - yellow
*/

html[data-theme=dark] .data-table-yellow {
    background: #a08839;
    color: #ffffff;
}

html[data-theme=dark] .data-table-yellow tr, 
html[data-theme=dark] tr.data-table-yellow, 
html[data-theme=dark] tr.data-table-yellow + tr {
    border-top: 1px solid #8e7318;
    vertical-align: top;
}

html[data-theme=dark] .data-table-yellow tr td, 
html[data-theme=dark] tr.data-table-yellow td, 
html[data-theme=dark] td.data-table-yellow {
    border-left: 1px solid #8e7318;
}

/*
** Infobox Pages
*/
html[data-theme=dark] .infobox {
    background: #545454;
    border: 1px solid #4f4f4f;
    color: #ffffff;
}

html[data-theme=dark] .infobox-header {
    background-color: #4a4642;
}

html[data-theme=dark] .infobox tr td {
    border: 1px solid #4f4f4f;
}

html[data-theme=dark] .container-purple {
    background: #765182;
    color: #ffffff;
    border: 1px solid #4f4f4f;
}

html[data-theme=dark] .container-green {
    background: #536746;
    color: #ffffff;
    border: 1px solid #4f4f4f;
}

html[data-theme=dark] .container-yellow {
    background: #a08839;
    color: #ffffff;
    border: 1px solid #4f4f4f;
}

html[data-theme=dark] .infobox-plain-heading {
    color: #ffffff;
    font-size: 0.85em;
    font-weight: bold;
    letter-spacing: 0.75px;
    text-transform: uppercase;
}

html[data-theme=dark] .infobox-table {
    background-color: #545454;
    color: #ffffff;
}

html[data-theme=dark] .infobox-table tr {
    border-top: 1px solid #151929;
}

html[data-theme=dark] .infobox-table-partition {
    border-collapse: collapse;
    color: #ffffff;
}

/*
** Template:Acquisition Sources
*/
html[data-theme=dark] .columns {
    column-rule: 1px solid #151929;
}

html[data-theme=dark] .column-category {
    border-top: 1px solid #151929;
}

/*
** Template:BadgeInfobox
*/
html[data-theme=dark] .badge-table {
    background-color: #545454;
    border-collapse: collapse;
}

html[data-theme=dark] .badge-table th:nth-child(1) {
    background-color: rgb(97, 90, 82);
    text-align: center;
}

html[data-theme=dark] .badge-table td:nth-child(odd) {
    background-color: rgb(97, 90, 82);
    text-align: center;
}

/* End dark mode rules */


/******************************\
**        DESKTOP RULES       **
\******************************/

@media (min-width: 768px) {

    .mobile-only {
        display: none;
    }

    /*
    ** Main Page
    */
    .featured-side-panel {
        width: 338px;
    }

    /*
    **  Infobox Pages
    */
    .infobox {
        width: 272px;
        margin: 9px;
    }

    /*
    ** Columns
    */
    .columns {
        column-count: 2;
        -webkit-column-count: 2;
        -moz-column-count: 2;
    }
    .column-category {
        page-break-inside: avoid;
        padding: 9px;
    }
    .big-category {
        column-span: all;
        column-count: 2;
        -webkit-column-count: 2;
        -moz-column-count: 2;
    }
    
    /*
    ** Containers
    */
    .container-flex {
        display: flex;
        min-width: 100px;
        margin: 9px 0px;
    }

    .container-table {
        display: table;
        margin: 9px 0px;
    }

    .container-row {
        display: block;
        margin: 9px;
    }

    .container {
        display: inline-block;
        margin: 9px;
        padding: 9px;
    }

    /* Override functionality if containers are grouped */
    .container-table .container-row {
        display: table-row;
        margin: 0px;
    }

    .container-table .container-row .container {
        display: table-cell;
        margin: 0px;
        padding: 9px;
    }

    .container-flex .container {
        display: block;
        margin: 0px;
        padding: 9px;
    }

    .spell-image {
        margin: 3px;
        width: 127px;
        height: 195px;
    }

    /*
    ** Template:CreatureInfobox
    */
    .monstrology-description {
        width: 40%;
        max-width: 400px;
        display: table-cell;
    }

    .monstrology-item {
        display: table-cell;
        width: 20%;
    }

    /*
    ** Template:PetInfobox
    */
    .ability-list {
        width: unset !important;
        min-width: 400px;
        max-width: 600px;
    }

    .list-container {
        margin: 9px;
        width: 272px;
    }

} /* End desktop rules */



/******************************\
**     LARGE SCREEN RULES     **
\******************************/

@media (min-width: 1280px) {

    /*
    ** Columns
    */
    .columns {
        column-count: 3;
        -webkit-column-count: 3;
        -moz-column-count: 3;
    }
    .column-category {
        page-break-inside: avoid;
        padding: 9px;
    }
    .big-category {
        column-span: all;
        column-count: 3;
        -webkit-column-count: 3;
        -moz-column-count: 3;
    }

}


/******************************\
**        MOBILE RULES        **
\******************************/

@media (max-width: 768px) {

    /*
    ** Adjustments to fix the positioning of the navigation bar on mobile devices
    */
    .navwrap {
        height: unset !important;
        position: unset !important;
    }
    
    .navC {
        height: unset !important;
    }
    
    #p-personal {
        position: unset !important;
    }
    
    #p-personal ul li {
        float: none !important;
        display: inline-block;
    }
    
    div#mw-page-base {
        display: none;
    }
    
    div#mw-head-base {
        display: none;
    }
    
    div#left-navigation {
        margin: unset !important;
    }
    
    div#mw-head {
        position: unset !important;
    }
    
    div#mw-navigation {
        min-height: 40px;
    }
    
    .mobilemenu {
        top: 9px !important;
    }
    /**** END MW-NAVIGATION FIX ****/

    #content {
        margin-left: 0 !important;
    }

    /*
    ** Search bar adjustment for mobile
    */
    div#simpleSearch {
        width: 100% !important;
    }

    /*
    ** Columns
    */
    .columns {
        column-count: 1;
        -webkit-column-count: 1;
        -moz-column-count: 1;
    }
    .column-category {
        page-break-inside: avoid;
        padding: 9px;
    }
    .big-category {
        column-span: all;
        column-count: 1;
        -webkit-column-count: 1;
        -moz-column-count: 1;
    }

    .desktop-only {
        display: none;
    }

    /*
    ** Embeds
    */
    div.thumbinner {
        width: unset !important; /* Prevents images from overflowing a mobile screen's dimensions */
    }

    /*
    ** Main Page
    */
    .featured-side-panel {
        width: 100%;
    }

    /*
    ** Special:RecentChanges
    */
    table.mw-recentchanges-table td {
        width: unset;
    }
    .mw-changeslist table.mw-enhanced-rc tr td:nth-child(1) {
        width: unset;
    }

    .mw-changeslist table.mw-enhanced-rc tr td.mw-enhanced-rc {
        width: unset;
    }

    span.comment {
        overflow-wrap: break-word;
        word-break: break-word;
    }

    /*
    ** Special:Ask
    */
    table.smw-ask-otheroptions tr td {
        display: inline-block;
        width: 100%;
    }

    /* Hide "extra" options on mobile */
    table.smw-ask-otheroptions tr:nth-child(n + 3), 
    table.smw-ask-otheroptions tr:nth-child(1) td:nth-child(n + 5), 
    table.smw-ask-otheroptions tr:nth-child(2) td:nth-child(n + 3) {
        display: none;
    }

    table.smw-ask-query th,
    table.smw-ask-query td {
        display: table-cell;
    }

    /*
    ** File pages
    */
    #filetoc li {
        padding: 0 1em;
    }
    .fullImageLink#file, 
    #mw-imagepage-section-filehistory {
        overflow-x: auto;
    }
    .mw-filepage-resolutioninfo, 
    #mw-imagepage-section-filehistory > p {
        position: sticky;
        left: 0;
        top: 0;
    }

    /*
    **  Data tables
    */
    table.data-table td {
        display: table-cell;
        width: unset; /* Override Vector skin rule */
    }

    /*
    **  Infobox Pages
    */
    .infobox {
        width: 100%;
        margin: 9px 0px;
    }
    
    /*
    ** Containers
    */
    .container-flex {
        margin: 9px 0px;
        display: block;
        clear: both;
    }

    .container-table {
        margin: 9px 0px;
        display: block;
        clear: both;
    }

    .container-row {
        display: block;
    }

    .container {
        display: block;
        padding: 9px;
    }

    .container-row .container {
        padding: 9px;
    }

    .spell-image {
        margin: 3px;
        width: calc(calc(100% - 24px) / 4); /* Show four images per row */
        min-width: 70px; /* Minimum width, in case images become too small */
        height: auto;
    }

    /*
    ** Template:DropInfobox2
    */
    div.drop-table div.drop-categories {
        column-count: 1; /* No more than one column should be displayed for mobile */
    }

    /*
    ** Template:CreatureInfobox
    */
    .monstrology-item {
        width: calc(100% / 3);
        min-height: 140px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }

    .cast-list {
        text-align: center;
    }

    /*
    ** Template:PetInfobox
    */
    .list-container {
        margin: 9px 0px;
        width: 100%;
    }

    /* AbilityList styles */
    .ability-list {
        width: 100%;
    }

    table.data-table td.ability-container {
        padding: 3px;
    }
}

@media (max-width: 850px) {
    /*
    ** MediaWiki:Sidebar
    */
    #mw-panel {
        display: none !important;
    }

} /* End mobile rules */

/******************************\
**        GLOBAL RULES        **
\******************************/

/*
** Content area rules
*/
#content.mw-body {
    /* Safari thinks text size is too small so it makes it bigger automatically - this resets that */
    -webkit-text-size-adjust: 100%;
}

#searchButton {
    border-radius: 0.5em;
}

/*
** Main Page
*/
.featured-side-panel {
    float: right;
}

/* Center site header notices */
.site-notice,
.user-notice,
.article-count {
    text-align: center;
}

.center-content {
    text-align: center;
}

/* Give space for the sorting controls on SMW tables */
table.sortable.wikitable tr th {
    padding-right: 1.6em !important;
}

/* Allow horizontal scroll on SMW tables when necessary */
.wikitable {
    display: block;
    overflow-x: auto;
}

/*
** Move Confirmation Page
*/
#mw-movepage-table {
    border: 0;
}

/*
** File pages
*/
.mw_metadata {
    margin: 9px 0px;
}

/*
** Table of Contents
*/
div#toc.toc {
    float: right;
    max-width: 300px;
    margin: 9px;
}


/*
** Thumbnail images
*/
.thumb {
    border: none;
    background: transparent;
}

div.thumbinner {
    color: #2c2c2c;
    background: #e3c790;
    background: rgba(146, 95, 0, 0.05);
    box-shadow: none;
    border: 0px;
    padding: 9px;
    margin-bottom: 9px;
}

div.thumbinner, 
div.thumbinner .image img {
    max-width: 100%;
    height: auto;
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

.CategoryTreeToggle {
    color: #ff9600;
}

hr.horizontal-clear {
    visibility: hidden;
    height: 0px;
    padding: 0px;
    margin: 0px;
    clear: both;
}

/* Admin Identifier */
.mw-userlink[title="User:AluraMist"],
.mw-userlink[title="User:Audacioussalix"],
.mw-userlink[title="User:CandyManXC11"],
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

.button {
    display: inline-block;
    position: relative;
    text-align: center;
    vertical-align: top;
}

.button > .button-link > a {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    opacity: 0;
}

.button.main-page-button {
    width: 85px;
    margin: 1em 9px;
}

/*
** Semantic Forms
*/
#sfForm {
    position: relative;
}

/*
** Textbox
*/
textarea {
    font-family: Monaco, monospace;
}

/*
** Infobox Pages
*/
.infobox {
    float: left;
    border-collapse: collapse;
}

.infobox-header {
    text-align: center;
    font-weight: bold;
}

table.infobox tr td {
    /* Override skin CSS */
    display: table-cell !important;
    width: unset !important;

    padding: 9px;
}

.infobox-hr {
    width: 100%;
    background: #cd8f52;
}

.infobox-accent-bordertop {
    background: rgba(146, 95, 0, 0.1);
    border-top: 1px solid #cd8f52;
}

.spell-image {
    display: inline-block;
}

.pvp-level-icon {
    position: relative;
}

.pvp-level-icon span {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -25%);
    color: #FFFF00; /* Yellow */
    font-size: 80%;
    font-weight: bold;
}

/*
** Infobox tables
*/
.infobox-table {
    display: inline-block;
    border-collapse: collapse;
    vertical-align: top;
}

.infobox-table tr th, .infobox-table tr td {
    padding: 9px;
}

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

/*
**  Data tables
*/
.data-table {
    width: 100%;
    border-collapse: collapse;
}
table.data-table th, table.data-table td {
    padding: 9px;
}
table .data-table {
    border: 0;  /* override border-top */
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
    padding: 9px;
}

.data-table-heading .mw-collapsible-toggle a {
    color: #fffcde;
}

.data-table-subheading {
    padding: 9px;
}

.data-table-faint {
    color: #9c8a92;
}


/*
** Data tables - normalizing
*/
.data-table tr:first-child {
    border-top: 0;
}
.data-table tr td:first-child {
    border-left: 0;
}

/*
** Containers
*/

.container-flex .container {
    flex-grow: 1;
}


/*
** Documentation pages
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

/*
** UI elements
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

/*
** Tool tip customization
*/
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

/*
** Main Page CSS
*/
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

/*
** Template CSS
*/
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

/*
** Template:CreatureInfobox
*/
.monstrology-item {
    text-align: center;
    vertical-align: middle;
}

/*
** Template:PetInfobox
*/
.pet-spell-image {
    margin: 3px;
}

.mw-collapsible-toggle {
    margin-left: 9px;
}

.pet-stats-table {
    margin: 9px 0px;
}

.pet-item-card {
    display: inline-block;
    width: 100px;
    text-align: center;
    vertical-align: top;
}

.ability-list {
    margin: 9px 0px;
}

.ability-image {
    width: 100%; /* Fill container */
    height: auto;
}

.list-container {
    display: block;
    float: left;
    clear: left;
    padding: 0px;
}

.list-container .container {
    margin: 0px;
    width: 100%;
}

/*
** Template:Acquisition Sources
*/
.columns {
    column-gap: 0px;
}

.creature-columns ul {
    column-gap: 25px;
}

.column-category {
    break-inside: avoid-column;
    page-break-inside: avoid;
    padding: 9px;
}

.span-columns {
    column-span: all;
}

/*
** Template:BadgeInfobox
*/
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

/*
** Template:PackInfobox + Template:FormatDropLinks
*/
.drop-tag {
    display: inline;
    padding-left: 5px;
    font-size: 0.85em;
}

.drop-tag:hover .wiki-tooltip {
    display: block;
}

.main-end {
    clear: both;
}/*
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