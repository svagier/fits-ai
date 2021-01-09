window.addEventListener("keydown", function(event) {
  if (event.defaultPrevented) {
    return; // Do nothing if event already handled
  }

  switch(event.code) {
    case "KeyR":
      rotateCurrentBlockClockwise();
      break;
    case "KeyE":
      rotateCurrentBlockCounterclockwise();
      break;
    case "KeyA":
    case "ArrowLeft":
      moveCurrentBlockLeft();
      break;
    case "KeyD":
    case "ArrowRight":
      moveCurrentBlockRight();
      break;
    case "KeyS":
    case "ArrowDown":
    case "Space":
      placeCurrentBlock();
      break;
  }

  // Consume the event so it doesn't get handled twice      // commented out since Ctrl+F5 didn't work
  // event.preventDefault();
}, true);