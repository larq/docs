// Re-render MathJax on document switch (instant loading, custom event)
document.addEventListener("DOMContentSwitch", function() {
  MathJax.typesetPromise();
});
