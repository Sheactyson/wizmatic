@media screen {
	/* Vector screen styles */
	/*
	 * Any rules which should not be flipped automatically in right-to-left situations should be
	 * prepended with @noflip in a comment block.
	 *
	 * This stylesheet employs a few CSS trick to accomplish compatibility with a wide range of web
	 * browsers. The most common trick is to use some styles in IE6 only. This is accomplished by using
	 * a rule that makes things work in IE6, and then following it with a rule that begins with
	 * "html > body" or use a child selector ">", which is ignored by IE6 because it does not support
	 * the child selector. You can spot this by looking for the "OVERRIDDEN BY COMPLIANT BROWSERS" and
	 * "IGNORED BY IE6" comments.
	 */
	/* Framework */
	html {
	  font-size: 100%;
	}
	html,
	body {
	  height: 100%;
	  margin: 0;
	  padding: 0;
	  font-family: sans-serif;
	}
	body {
	  background-color: #f6f6f6;
	}
	/* Content */
	.mw-body {
	  margin-left: 10em;
	  padding: 1em;
	  /* Border on top, left, and bottom side */
	  border: 1px solid #a7d7f9;
	  border-right-width: 0;
	  /* Merge the border with tabs' one (in their background image) */
	  margin-top: -1px;
	  background-color: #ffffff;
	  color: #252525;
	  direction: ltr;
	}
	.mw-body .mw-editsection,
	.mw-body .mw-editsection-like {
	  font-family: sans-serif;
	}
	.mw-body p {
	  line-height: inherit;
	  margin: 0.5em 0;
	}
	.mw-body h1,
	.mw-body h2 {
	  font-family: "Linux Libertine", Georgia, Times, serif;
	  line-height: 1.3;
	  margin-bottom: 0.25em;
	  padding: 0;
	  /* Fallback heading font for scripts which render poorly in @content-heading-font-family. */
	  /* See T73240 */
	}
	.mw-body h1:lang( ja ),
	.mw-body h2:lang( ja ),
	.mw-body h1:lang( he ),
	.mw-body h2:lang( he ),
	.mw-body h1:lang( ko ),
	.mw-body h2:lang( ko ) {
	  /* See T65827 */
	  font-family: sans-serif;
	}
	.mw-body h1 {
	  font-size: 1.8em;
	}
	.mw-body .mw-body-content h1 {
	  margin-top: 1em;
	}
	.mw-body h2 {
	  font-size: 1.5em;
	  margin-top: 1em;
	}
	.mw-body h3,
	.mw-body h4,
	.mw-body h5,
	.mw-body h6 {
	  line-height: 1.6;
	  margin-top: 0.3em;
	  margin-bottom: 0;
	  padding-bottom: 0;
	}
	.mw-body h3 {
	  font-size: 1.2em;
	}
	.mw-body h3,
	.mw-body h4 {
	  font-weight: bold;
	}
	.mw-body h4,
	.mw-body h5,
	.mw-body h6 {
	  font-size: 100%;
	  /* (reset) */
	}
	.mw-body #toc h2,
	.mw-body .toc h2 {
	  font-size: 100%;
	  /* (reset) */
	  font-family: sans-serif;
	}
	.mw-body .firstHeading {
	  /* Change the default from mediawiki.skinning CSS to let indicators float into heading area */
	  overflow: visible;
	}
	.mw-body .mw-indicators {
	  float: right;
	  line-height: 1.6;
	  font-size: 0.875em;
	  /* Ensure that this is displayed on top of .mw-body-content and clickable */
	  position: relative;
	  z-index: 1;
	}
	.mw-body .mw-indicator {
	  display: inline-block;
	  zoom: 1;
	  *display: inline;
	}
	/* Hide empty portlets */
	div.emptyPortlet {
	  display: none;
	}
	ul {
	  list-style-type: disc;
	  list-style-image: url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20version%3D%221.1%22%20width%3D%225%22%20height%3D%2213%22%3E%0A%3Ccircle%20cx%3D%222.5%22%20cy%3D%229.5%22%20r%3D%222.5%22%20fill%3D%22%2300528c%22%2F%3E%0A%3C%2Fsvg%3E%0A);
	  list-style-image: url(/wiki/skins/Vector/images/bullet-icon.svg?90d59)!ie;
	  /* Fallback to PNG bullet for IE 8 and below using CSS hack */
	  list-style-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAANCAIAAADuXjPfAAAABnRSTlMA/wD/AP83WBt9AAAAHklEQVR4AWP4jwrowWcI6oEgEBtIISNCfFT9mOYDACO/lbNIGC/yAAAAAElFTkSuQmCC) \9;
	  /* Fallback to PNG bullet for IE 8 and below using CSS hack */
	  list-style-image: url(/wiki/skins/Vector/images/bullet-icon.png?e31f8) \9!ie;
	}
	pre,
	.mw-code {
	  line-height: 1.3em;
	}
	/* Site Notice (includes notices from CentralNotice extension) */
	#siteNotice {
	  font-size: 0.8em;
	}
	.redirectText {
	  font-size: 140%;
	}
	.redirectMsg p {
	  margin: 0;
	}
	.mw-body-content {
	  position: relative;
	  line-height: 1.6;
	  font-size: 0.875em;
	  z-index: 0;
	}
	/* Personal */
	#p-personal {
	  position: absolute;
	  top: 0.33em;
	  right: 0.75em;
	  /* Display on top of page tabs - bugs 37158, 48078 */
	  z-index: 100;
	}
	#p-personal h3 {
	  display: none;
	}
	#p-personal ul {
	  list-style-type: none;
	  list-style-image: none;
	  margin: 0;
	  padding-left: 10em;
	  /* Keep from overlapping logo */
	}
	#p-personal li {
	  line-height: 1.125em;
	  /* @noflip */
	  float: left;
	  margin-left: 0.75em;
	  margin-top: 0.5em;
	  font-size: 0.75em;
	  white-space: nowrap;
	}
	/* Icon for Usernames */
	#pt-userpage,
	#pt-anonuserpage {
	  background-position: left top;
	  background-repeat: no-repeat;
	  /* SVG support using a transparent gradient to guarantee cross-browser
		 * compatibility (browsers able to understand gradient syntax support also SVG) */
	  background-image: url(/wiki/skins/Vector/images/user-icon.png?13155);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22utf-8%22%3F%3E%0A%3C%21DOCTYPE%20svg%20PUBLIC%20%22-%2F%2FW3C%2F%2FDTD%20SVG%201.1%2F%2FEN%22%20%22http%3A%2F%2Fwww.w3.org%2FGraphics%2FSVG%2F1.1%2FDTD%2Fsvg11.dtd%22%3E%0A%3Csvg%20version%3D%221.1%22%20id%3D%22Layer_1%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20x%3D%220px%22%20y%3D%220px%22%0A%09%20width%3D%2212px%22%20height%3D%2213.836px%22%20viewBox%3D%220%200%2012%2013.836%22%20enable-background%3D%22new%200%200%2012%2013.836%22%20xml%3Aspace%3D%22preserve%22%3E%0A%3Cpath%20fill%3D%22%23777777%22%20d%3D%22M1.938%2C6.656c-1.32%2C1.485-1.47%2C3.15-0.97%2C4.25c0.323%2C0.707%2C0.78%2C1.127%2C1.313%2C1.375%0A%09c0.496%2C0.229%2C1.074%2C0.273%2C1.658%2C0.282c0.023%2C0%2C0.04%2C0.03%2C0.062%2C0.03h4.187c0.61%2C0%2C1.225-0.125%2C1.75-0.405%0A%09c0.527-0.28%2C0.961-0.718%2C1.188-1.376c0.335-0.964%2C0.175-2.529-1.094-4.03C9.094%2C7.954%2C7.68%2C8.719%2C6.065%2C8.719%0A%09c-1.677%2C0-3.182-0.812-4.125-2.063H1.938z%22%2F%3E%0A%3Cpath%20fill%3D%22%23777777%22%20d%3D%22M6.063%2C0c-1.89%2C0-3.595%2C1.674-3.594%2C3.563C2.467%2C5.45%2C4.173%2C7.155%2C6.06%2C7.155%0A%09c1.89%2C0%2C3.564-1.705%2C3.563-3.593C9.625%2C1.673%2C7.95%2C0%2C6.063%2C0L6.063%2C0z%22%2F%3E%0A%3C%2Fsvg%3E%0A);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/user-icon.svg?7b5d5)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/user-icon.png?13155);
	  padding-left: 15px !important;
	}
	/* Show "Not logged in" text in gray */
	#pt-anonuserpage {
	  color: #707070;
	}
	/* Search */
	#p-search {
	  /* @noflip */
	  float: left;
	  margin-right: 0.5em;
	  margin-left: 0.5em;
	}
	#p-search h3 {
	  display: block;
	  position: absolute !important;
	  clip: rect(1px, 1px, 1px, 1px);
	  width: 1px;
	  height: 1px;
	  margin: -1px;
	  border: 0;
	  padding: 0;
	  overflow: hidden;
	}
	#p-search form,
	#p-search input {
	  margin: 0;
	  margin-top: 0.4em;
	}
	div#simpleSearch {
	  display: block;
	  width: 12.6em;
	  width: 20vw;
	  /* responsive width */
	  min-width: 5em;
	  max-width: 20em;
	  padding-right: 1.4em;
	  height: 1.4em;
	  margin-top: 0.65em;
	  position: relative;
	  min-height: 1px;
	  /* Gotta trigger hasLayout for IE7 */
	  border: solid 1px #aaa;
	  color: black;
	  background-color: white;
	  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAQCAIAAABY/YLgAAAAJUlEQVQIHQXBsQEAAAjDoND/73UWdnerhmHVsDQZJrNWVg3Dqge6bgMe6bejNAAAAABJRU5ErkJggg==);
	  background-image: url(/wiki/skins/Vector/images/search-fade.png?50f7b)!ie;
	  background-position: top left;
	  background-repeat: repeat-x;
	}
	div#simpleSearch input {
	  margin: 0;
	  padding: 0;
	  border: 0;
	  background-color: transparent;
	  color: black;
	}
	div#simpleSearch #searchInput {
	  width: 100%;
	  padding: 0.2em 0 0.2em 0.2em;
	  font-size: 13px;
	  direction: ltr;
	  -webkit-appearance: textfield;
	}
	div#simpleSearch #searchInput:focus {
	  outline: none;
	}
	div#simpleSearch #searchInput.placeholder {
	  color: #999;
	}
	div#simpleSearch #searchInput:-ms-input-placeholder {
	  color: #999;
	}
	div#simpleSearch #searchInput:-moz-placeholder {
	  color: #999;
	}
	div#simpleSearch #searchInput::-webkit-search-decoration,
	div#simpleSearch #searchInput::-webkit-search-cancel-button,
	div#simpleSearch #searchInput::-webkit-search-results-button,
	div#simpleSearch #searchInput::-webkit-search-results-decoration {
	  -webkit-appearance: textfield;
	}
	div#simpleSearch #searchButton,
	div#simpleSearch #mw-searchButton {
	  position: absolute;
	  top: 0;
	  right: 0;
	  width: 1.65em;
	  height: 100%;
	  cursor: pointer;
	  /* Hide button text and replace it with the image. */
	  text-indent: -99999px;
	  /* Needed to make IE6 respect the text-indent. */
	  line-height: 1;
	  /* Opera 12 on RTL flips the text in a funny way without this. */
	  /* @noflip */
	  direction: ltr;
	  white-space: nowrap;
	  overflow: hidden;
	}
	div#simpleSearch #searchButton {
	  background-image: url(/wiki/skins/Vector/images/search-ltr.png?39f97);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2212%22%20height%3D%2213%22%3E%3Cg%20stroke-width%3D%222%22%20stroke%3D%22%236c6c6c%22%20fill%3D%22none%22%3E%3Cpath%20d%3D%22M11.29%2011.71l-4-4%22%2F%3E%3Ccircle%20cx%3D%225%22%20cy%3D%225%22%20r%3D%224%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/search-ltr.svg?07752)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/search-ltr.png?39f97);
	  background-position: center center;
	  background-repeat: no-repeat;
	}
	div#simpleSearch #mw-searchButton {
	  z-index: 1;
	}
	/*
	Styling for namespace tabs (page, discussion) and views (read, edit, view history, watch and other actions)
	*/
	/* Navigation Labels */
	div.vectorTabs h3 {
	  display: none;
	}
	/* Namespaces and Views */
	div.vectorTabs {
	  /* @noflip */
	  float: left;
	  height: 2.5em;
	  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAuCAIAAABmjeQ9AAAAQ0lEQVR4AWVOhQEAIAzC/X+xAXbXeoDFGA3A9yk1n4juBROcUegfarWjP3ojZvEzxs6j+nygmo+zzsk79nY+tOxdEhlf3UHVgUFrVwAAAABJRU5ErkJggg==);
	  background-image: url(/wiki/skins/Vector/images/tab-break.png?09d4b)!ie;
	  background-position: bottom left;
	  background-repeat: no-repeat;
	  padding-left: 1px;
	}
	div.vectorTabs ul {
	  /* @noflip */
	  float: left;
	  height: 100%;
	  list-style-type: none;
	  list-style-image: none;
	  margin: 0;
	  padding: 0;
	  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAuCAIAAABmjeQ9AAAAQ0lEQVR4AWVOhQEAIAzC/X+xAXbXeoDFGA3A9yk1n4juBROcUegfarWjP3ojZvEzxs6j+nygmo+zzsk79nY+tOxdEhlf3UHVgUFrVwAAAABJRU5ErkJggg==);
	  background-image: url(/wiki/skins/Vector/images/tab-break.png?09d4b)!ie;
	  background-position: right bottom;
	  background-repeat: no-repeat;
	  /* IGNORED BY IE6 which doesn't support child selector */
	}
	div.vectorTabs ul li {
	  /* @noflip */
	  float: left;
	  line-height: 1.125em;
	  /* For IE6, overridden later to display:block by modern browsers */
	  display: inline-block;
	  height: 100%;
	  margin: 0;
	  padding: 0;
	  background-color: #f3f3f3;
	  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAABkCAIAAADITs03AAAAO0lEQVR4AeSKhREAMQzDdN5/5uixuEKDpqgBjl2f78wd2DVj1+26/h///PfteVMN7zoGebcg1/Y/ZQQAlAUtQCujIJMAAAAASUVORK5CYII=);
	  background-image: url(/wiki/skins/Vector/images/tab-normal-fade.png?1cc52)!ie;
	  background-position: bottom left;
	  background-repeat: repeat-x;
	  white-space: nowrap;
	}
	div.vectorTabs ul > li {
	  display: block;
	}
	div.vectorTabs li {
	  /* Ignored by IE6 which doesn't support child selector */
	}
	div.vectorTabs li.new a,
	div.vectorTabs li.new a:visited {
	  color: #a55858;
	}
	div.vectorTabs li.selected {
	  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAABkAQAAAABvV2fNAAAADElEQVR4AWNoGB4QAInlMgFKeRKBAAAAAElFTkSuQmCC);
	  background-image: url(/wiki/skins/Vector/images/tab-current-fade.png?22887)!ie;
	}
	div.vectorTabs li.selected a,
	div.vectorTabs li.selected a:visited {
	  color: #333;
	  text-decoration: none;
	}
	div.vectorTabs li.icon a {
	  background-position: bottom right;
	  background-repeat: no-repeat;
	}
	div.vectorTabs li a {
	  /* For IE6, overridden later to display:block by modern browsers */
	  display: inline-block;
	  height: 1.9em;
	  padding-left: 0.5em;
	  padding-right: 0.5em;
	  color: #0645ad;
	  cursor: pointer;
	  font-size: 0.8em;
	}
	div.vectorTabs li > a {
	  display: block;
	}
	div.vectorTabs span {
	  display: inline-block;
	  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAuCAIAAABmjeQ9AAAAQ0lEQVR4AWVOhQEAIAzC/X+xAXbXeoDFGA3A9yk1n4juBROcUegfarWjP3ojZvEzxs6j+nygmo+zzsk79nY+tOxdEhlf3UHVgUFrVwAAAABJRU5ErkJggg==);
	  background-image: url(/wiki/skins/Vector/images/tab-break.png?09d4b)!ie;
	  background-position: bottom right;
	  background-repeat: no-repeat;
	  /* Ignored by IE6 which doesn't support child selector */
	}
	div.vectorTabs span a {
	  /* For IE6, overridden later to display:block by modern browsers */
	  display: inline-block;
	  padding-top: 1.25em;
	}
	div.vectorTabs span > a {
	  /* @noflip */
	  float: left;
	  display: block;
	}
	/* Variants and Actions */
	div.vectorMenu {
	  /* @noflip */
	  direction: ltr;
	  /* @noflip */
	  float: left;
	  cursor: pointer;
	  position: relative;
	}
	body.rtl div.vectorMenu {
	  /* @noflip */
	  direction: rtl;
	}
	div#mw-head div.vectorMenu h3 {
	  /* @noflip */
	  float: left;
	  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAuCAIAAABmjeQ9AAAAQ0lEQVR4AWVOhQEAIAzC/X+xAXbXeoDFGA3A9yk1n4juBROcUegfarWjP3ojZvEzxs6j+nygmo+zzsk79nY+tOxdEhlf3UHVgUFrVwAAAABJRU5ErkJggg==);
	  background-image: url(/wiki/skins/Vector/images/tab-break.png?09d4b)!ie;
	  background-repeat: no-repeat;
	  background-position: bottom right;
	  font-size: 1em;
	  height: 2.5em;
	  padding-right: 1px;
	  margin-right: -1px;
	}
	div.vectorMenu h3 span {
	  display: block;
	  font-size: 0.8em;
	  padding-left: 0.7em;
	  padding-top: 1.375em;
	  margin-right: 20px;
	  font-weight: normal;
	  color: #4d4d4d;
	}
	div.vectorMenu h3 a {
	  position: absolute;
	  top: 0;
	  right: 0;
	  width: 20px;
	  height: 2.5em;
	  background-image: url(/wiki/skins/Vector/images/arrow-down-icon.png?d72f0);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2222%22%20height%3D%2216%22%3E%3Cpath%20d%3D%22M15.502%206.001l-5%205.001-5-5.001z%22%20fill%3D%22%23797979%22%2F%3E%3C%2Fsvg%3E);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/arrow-down-icon.svg?92f5b)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/arrow-down-icon.png?d72f0);
	  background-position: 100% 70%;
	  background-repeat: no-repeat;
	  -webkit-transition: background-position 250ms;
	  -moz-transition: background-position 250ms;
	  transition: background-position 250ms;
	}
	div.vectorMenu.menuForceShow h3 a {
	  background-position: 100% 100%;
	}
	div.vectorMenuFocus h3 a {
	  background-image: url(/wiki/skins/Vector/images/arrow-down-focus-icon.png?69899);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2222%22%20height%3D%2216%22%3E%3Cpath%20d%3D%22M15.502%206.001l-5%205.001-5-5.001z%22%20fill%3D%22%23929292%22%2F%3E%3C%2Fsvg%3E);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/arrow-down-focus-icon.svg?6cc06)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/arrow-down-focus-icon.png?69899);
	}
	div.vectorMenu div.menu {
	  min-width: 100%;
	  position: absolute;
	  top: 2.5em;
	  left: -1px;
	  background-color: white;
	  border: solid 1px silver;
	  border-top-width: 0;
	  clear: both;
	  text-align: left;
	  display: none;
	  z-index: 1;
	}
	/* Enable forcing showing of the menu for accessibility */
	div.vectorMenu:hover div.menu,
	div.vectorMenu.menuForceShow div.menu {
	  display: block;
	}
	div.vectorMenu ul {
	  list-style-type: none;
	  list-style-image: none;
	  padding: 0;
	  margin: 0;
	  text-align: left;
	}
	/* Fixes old versions of FireFox */
	div.vectorMenu ul,
	x:-moz-any-link {
	  min-width: 5em;
	}
	/* Returns things back to normal in modern versions of FireFox */
	div.vectorMenu ul,
	x:-moz-any-link,
	x:default {
	  min-width: 0;
	}
	div.vectorMenu li {
	  padding: 0;
	  margin: 0;
	  text-align: left;
	  line-height: 1em;
	}
	/* OVERRIDDEN BY COMPLIANT BROWSERS */
	div.vectorMenu li a {
	  display: inline-block;
	  padding: 0.5em;
	  white-space: nowrap;
	  color: #0645ad;
	  cursor: pointer;
	  font-size: 0.8em;
	}
	/* IGNORED BY IE6 */
	div.vectorMenu li > a {
	  display: block;
	}
	div.vectorMenu li.selected a,
	div.vectorMenu li.selected a:visited {
	  color: #333;
	  text-decoration: none;
	}
	* html div.vectorMenu div.menu {
	  display: block;
	  position: static;
	  border: 0;
	}
	* html div#mw-head div.vectorMenu h3 {
	  display: none;
	}
	* html div.vectorMenu li {
	  float: left;
	  line-height: 1.125em;
	  border-right: 1px solid #a7d7f9;
	}
	* html div.vectorMenu li a {
	  padding-top: 1.25em;
	}
	@-webkit-keyframes rotate {
	  from {
	    -webkit-transform: rotate(0deg);
	    -moz-transform: rotate(0deg);
	    transform: rotate(0deg);
	  }
	  to {
	    -webkit-transform: rotate(360deg);
	    -moz-transform: rotate(360deg);
	    transform: rotate(360deg);
	  }
	}
	@-moz-keyframes rotate {
	  from {
	    -webkit-transform: rotate(0deg);
	    -moz-transform: rotate(0deg);
	    transform: rotate(0deg);
	  }
	  to {
	    -webkit-transform: rotate(360deg);
	    -moz-transform: rotate(360deg);
	    transform: rotate(360deg);
	  }
	}
	@keyframes rotate {
	  from {
	    -webkit-transform: rotate(0deg);
	    -moz-transform: rotate(0deg);
	    transform: rotate(0deg);
	  }
	  to {
	    -webkit-transform: rotate(360deg);
	    -moz-transform: rotate(360deg);
	    transform: rotate(360deg);
	  }
	}
	/* Watch/Unwatch Icon Styling */
	#ca-unwatch.icon a,
	#ca-watch.icon a {
	  margin: 0;
	  padding: 0;
	  display: block;
	  width: 26px;
	  /* This hides the text but shows the background image */
	  padding-top: 3.1em;
	  margin-top: 0;
	  /* Only applied in IE6 */
	  _margin-top: -0.8em;
	  height: 0;
	  overflow: hidden;
	  background-position: 5px 60%;
	}
	#ca-unwatch.icon a {
	  background-image: url(/wiki/skins/Vector/images/unwatch-icon.png?fccbe);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20width%3D%2216%22%20height%3D%2216%22%3E%3Cdefs%3E%3ClinearGradient%20id%3D%22a%22%3E%3Cstop%20offset%3D%220%22%20stop-color%3D%22%23c2edff%22%2F%3E%3Cstop%20offset%3D%22.5%22%20stop-color%3D%22%2368bdff%22%2F%3E%3Cstop%20offset%3D%221%22%20stop-color%3D%22%23fff%22%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient%20x1%3D%2213.47%22%20y1%3D%2214.363%22%20x2%3D%224.596%22%20y2%3D%223.397%22%20id%3D%22b%22%20xlink%3Ahref%3D%22%23a%22%20gradientUnits%3D%22userSpaceOnUse%22%2F%3E%3C%2Fdefs%3E%3Cpath%20d%3D%22M8.103%201.146l2.175%204.408%204.864.707-3.52%203.431.831%204.845-4.351-2.287-4.351%202.287.831-4.845-3.52-3.431%204.864-.707z%22%20fill%3D%22url%28%23b%29%22%20stroke%3D%22%237cb5d1%22%20stroke-width%3D%220.9999199999999999%22%2F%3E%3C%2Fsvg%3E);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/unwatch-icon.svg?95d18)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/unwatch-icon.png?fccbe);
	}
	#ca-watch.icon a {
	  background-image: url(/wiki/skins/Vector/images/watch-icon.png?e1b42);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%3E%3Cpath%20d%3D%22M8.103%201.146l2.175%204.408%204.864.707-3.52%203.431.831%204.845-4.351-2.287-4.351%202.287.831-4.845-3.52-3.431%204.864-.707z%22%20fill%3D%22%23fff%22%20stroke%3D%22%237cb5d1%22%20stroke-width%3D%220.9999199999999999%22%2F%3E%3C%2Fsvg%3E);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/watch-icon.svg?200b7)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/watch-icon.png?e1b42);
	}
	#ca-unwatch.icon a:hover,
	#ca-unwatch.icon a:focus {
	  background-image: url(/wiki/skins/Vector/images/unwatch-icon-hl.png?c4723);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20width%3D%2216%22%20height%3D%2216%22%3E%3Cdefs%3E%3ClinearGradient%20id%3D%22a%22%3E%3Cstop%20offset%3D%220%22%20stop-color%3D%22%23c2edff%22%2F%3E%3Cstop%20offset%3D%22.5%22%20stop-color%3D%22%2368bdff%22%2F%3E%3Cstop%20offset%3D%221%22%20stop-color%3D%22%23fff%22%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient%20x1%3D%2213.47%22%20y1%3D%2214.363%22%20x2%3D%224.596%22%20y2%3D%223.397%22%20id%3D%22b%22%20xlink%3Ahref%3D%22%23a%22%20gradientUnits%3D%22userSpaceOnUse%22%2F%3E%3C%2Fdefs%3E%3Cpath%20d%3D%22M8.103%201.146l2.175%204.408%204.864.707-3.52%203.431.831%204.845-4.351-2.287-4.351%202.287.831-4.845-3.52-3.431%204.864-.707z%22%20fill%3D%22url%28%23b%29%22%20stroke%3D%22%23c8b250%22%20stroke-width%3D%220.9999199999999999%22%2F%3E%3C%2Fsvg%3E);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/unwatch-icon-hl.svg?a3932)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/unwatch-icon-hl.png?c4723);
	}
	#ca-watch.icon a:hover,
	#ca-watch.icon a:focus {
	  background-image: url(/wiki/skins/Vector/images/watch-icon-hl.png?f4c7e);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%3E%3Cpath%20d%3D%22M8.103%201.146l2.175%204.408%204.864.707-3.52%203.431.831%204.845-4.351-2.287-4.351%202.287.831-4.845-3.52-3.431%204.864-.707z%22%20fill%3D%22%23fff%22%20stroke%3D%22%23c8b250%22%20stroke-width%3D%220.9999199999999999%22%2F%3E%3C%2Fsvg%3E);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/watch-icon-hl.svg?2b77d)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/watch-icon-hl.png?f4c7e);
	}
	#ca-unwatch.icon a.loading,
	#ca-watch.icon a.loading {
	  background-image: url(/wiki/skins/Vector/images/watch-icon-loading.png?5cb92);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%3E%3Cpath%20d%3D%22M8.103%201.146l2.175%204.408%204.864.707-3.52%203.431.831%204.845-4.351-2.287-4.351%202.287.831-4.845-3.52-3.431%204.864-.707z%22%20fill%3D%22%23fff%22%20stroke%3D%22%23d1d1d1%22%20stroke-width%3D%220.9999199999999999%22%2F%3E%3C%2Fsvg%3E);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/watch-icon-loading.svg?6ca63)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/watch-icon-loading.png?5cb92);
	  -webkit-animation: rotate 700ms infinite linear;
	  -moz-animation: rotate 700ms infinite linear;
	  -o-animation: rotate 700ms infinite linear;
	  animation: rotate 700ms infinite linear;
	  /* Suppress the hilarious rotating focus outline on Firefox */
	  outline: none;
	  cursor: default;
	  pointer-events: none;
	  background-position: 50% 60%;
	  -webkit-transform-origin: 50% 57%;
	  transform-origin: 50% 57%;
	}
	#ca-unwatch.icon a span,
	#ca-watch.icon a span {
	  display: none;
	}
	/* Hide, but keep accessible for screen-readers */
	#mw-navigation h2 {
	  position: absolute;
	  top: -9999px;
	}
	/* Head */
	#mw-page-base {
	  height: 5em;
	  background-position: bottom left;
	  background-repeat: repeat-x;
	  /* This image is only a fallback (for IE 6-9), so we do not @embed it. */
	  background-image: url(/wiki/skins/Vector/images/page-fade.png?1d168);
	  background-color: #f6f6f6;
	  background-image: -webkit-gradient(linear, left top, left bottom, color-stop(50%, #ffffff), color-stop(100%, #f6f6f6));
	  background-image: -webkit-linear-gradient(top, #ffffff 50%, #f6f6f6 100%);
	  background-image: -moz-linear-gradient(top, #ffffff 50%, #f6f6f6 100%);
	  background-image: linear-gradient(#ffffff 50%, #f6f6f6 100%);
	  background-color: #ffffff;
	}
	#mw-head-base {
	  margin-top: -5em;
	  margin-left: 10em;
	  height: 5em;
	}
	div#mw-head {
	  position: absolute;
	  top: 0;
	  right: 0;
	  width: 100%;
	}
	div#mw-head h3 {
	  margin: 0;
	  padding: 0;
	}
	/* Navigation Containers */
	#left-navigation {
	  float: left;
	  margin-left: 10em;
	  margin-top: 2.5em;
	  /* When right nav would overlap left nav, it's placed below it
		   (normal CSS floats behavior). This rule ensures that no empty space
		   is shown between them due to right nav's margin-top. Page layout
		   is still broken, but at least the nav overlaps only the page title
		   instead of half the content. */
	  margin-bottom: -2.5em;
	  /* IE 6 double-margin bug fix */
	  display: inline;
	}
	#right-navigation {
	  float: right;
	  margin-top: 2.5em;
	}
	/* Logo */
	#p-logo {
	  position: absolute;
	  top: -160px;
	  left: 0;
	  width: 10em;
	  height: 160px;
	}
	#p-logo a {
	  display: block;
	  width: 10em;
	  height: 160px;
	  background-repeat: no-repeat;
	  background-position: center center;
	  text-decoration: none;
	}
	/* Panel */
	div#mw-panel {
	  font-size: inherit;
	  position: absolute;
	  top: 160px;
	  padding-top: 1em;
	  width: 10em;
	  left: 0;
	  /* First sidebar portlet. Not using :first-of-type for IE<=8 support. */
	}
	div#mw-panel div.portal {
	  margin: 0 0.6em 0 0.7em;
	  padding: 0.25em 0;
	  direction: ltr;
	  background-position: top left;
	  background-repeat: no-repeat;
	  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIwAAAABCAAAAAAphRnkAAAAJ0lEQVQIW7XFsQEAIAyAMPD/b7uLWz8wS5youFW1UREfiIpH1Q2VBz7fGPS1dOGeAAAAAElFTkSuQmCC);
	  background-image: url(/wiki/skins/Vector/images/portal-break.png?3ea1b)!ie;
	}
	div#mw-panel div.portal h3 {
	  font-size: 0.75em;
	  color: #4d4d4d;
	  font-weight: normal;
	  margin: 0;
	  padding: 0.25em 0 0.25em 0.25em;
	  cursor: default;
	  border: none;
	}
	div#mw-panel div.portal div.body {
	  margin: 0 0 0 1.25em;
	  padding-top: 0;
	}
	div#mw-panel div.portal div.body ul {
	  list-style-type: none;
	  list-style-image: none;
	  margin: 0;
	  padding: 0;
	}
	div#mw-panel div.portal div.body ul li {
	  line-height: 1.125em;
	  margin: 0;
	  padding: 0.25em 0;
	  font-size: 0.75em;
	  word-wrap: break-word;
	}
	div#mw-panel div.portal div.body ul li a {
	  color: #0645ad;
	}
	div#mw-panel div.portal div.body ul li a:visited {
	  color: #0b0080;
	}
	div#mw-panel #p-logo + div.portal {
	  background-image: none;
	  margin-top: 0;
	}
	div#mw-panel #p-logo + div.portal h3 {
	  display: none;
	}
	div#mw-panel #p-logo + div.portal div.body {
	  margin-left: 0.5em;
	}
	/* Footer */
	div#footer {
	  margin-left: 10em;
	  margin-top: 0;
	  padding: 0.75em;
	  direction: ltr;
	}
	div#footer ul {
	  list-style-type: none;
	  list-style-image: none;
	  margin: 0;
	  padding: 0;
	}
	div#footer ul li {
	  margin: 0;
	  padding: 0;
	  padding-top: 0.5em;
	  padding-bottom: 0.5em;
	  color: #333;
	  font-size: 0.7em;
	}
	div#footer #footer-icons {
	  float: right;
	}
	div#footer #footer-icons li {
	  float: left;
	  margin-left: 0.5em;
	  line-height: 2em;
	  text-align: right;
	}
	div#footer #footer-info li {
	  line-height: 1.4em;
	}
	div#footer #footer-places li {
	  float: left;
	  margin-right: 1em;
	  line-height: 2em;
	}
	body.ltr div#footer #footer-places {
	  /* @noflip */
	  float: left;
	}
	.mw-body .external {
	  background-position: center right;
	  background-repeat: no-repeat;
	  background-image: url(/wiki/skins/Vector/images/external-link-ltr-icon.png?325de);
	  background-image: linear-gradient(transparent, transparent), url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%20standalone%3D%22no%22%3F%3E%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2212%22%20height%3D%2212%22%3E%3Cpath%20fill%3D%22%23fff%22%20stroke%3D%22%2306c%22%20d%3D%22M1.5%204.518h5.982V10.5H1.5z%22%2F%3E%3Cpath%20d%3D%22M5.765%201H11v5.39L9.427%207.937l-1.31-1.31L5.393%209.35l-2.69-2.688%202.81-2.808L4.2%202.544z%22%20fill%3D%22%2306f%22%2F%3E%3Cpath%20d%3D%22M9.995%202.004l.022%204.885L8.2%205.07%205.32%207.95%204.09%206.723l2.882-2.88-1.85-1.852z%22%20fill%3D%22%23fff%22%2F%3E%3C%2Fsvg%3E);
	  background-image: linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/external-link-ltr-icon.svg?13447)!ie;
	  background-image: -o-linear-gradient(transparent, transparent), url(/wiki/skins/Vector/images/external-link-ltr-icon.png?325de);
	  padding-right: 13px;
	}}@media screen and (min-width: 982px) {
	/* Vector screen styles for high definition displays */
	.mw-body {
	  margin-left: 11em;
	  padding: 1.25em 1.5em 1.5em 1.5em;
	}
	#p-logo {
	  left: 0.5em;
	}
	div#footer {
	  margin-left: 11em;
	  padding: 1.25em;
	}
	#mw-panel {
	  padding-left: 0.5em;
	}
	#p-search {
	  margin-right: 1em;
	}
	#left-navigation {
	  margin-left: 11em;
	}
	#p-personal {
	  right: 1em;
	}
	#mw-head-base {
	  margin-left: 11em;
	}}