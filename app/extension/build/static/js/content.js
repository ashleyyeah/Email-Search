!function(){"use strict";var e;!function(e){e[e.React=0]="React",e[e.Content=1]="Content"}(e||(e={}));var n=function(n,t,o){var r=function(n,t){return t.id===chrome.runtime.id&&n.from===e.React}(n,t);if(r&&"Hello from React"===n.message&&o("Hello from content.js"),r&&"delete logo"===n.message){var l,c=document.getElementById("hplogo");null===c||void 0===c||null===(l=c.parentElement)||void 0===l||l.removeChild(c)}};console.log("[content.ts] Main"),chrome.runtime.onMessage.addListener(n)}();
//# sourceMappingURL=content.js.map