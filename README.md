# Rotorhazard Pilot Photos
A RotorHazard plugin which adds a pilot card stream element which showcases a photo and both primary and optional secondary color

## Help your livestream viewers put faces to names
![alt text](https://github.com/skyfpv/rh_pilot_photos/blob/main/docs/images/streamElementsExample.jpg?raw=true)
use the url http://rotorhazard.local/stream/pilotphoto/1 to view the first pilot card
## Easy setup via new pilot attributes
![alt text](https://github.com/skyfpv/rh_pilot_photos/blob/main/docs/images/pilotAttributes.jpg?raw=true)
## Set up in OBS works just like any other rotorhazard stream element

![alt text](https://github.com/skyfpv/rh_pilot_photos/blob/main/docs/images/streamElementsExample2.jpg?raw=true)
Create a browser source and use the url http://rotorhazard.local/stream/pilotphoto/[DESIRED_NODE_NUMBER] to show the card for each of the available nodes. Create browser source per pilot card. 
We recommend the following settings for the browser source.
- width: 432
- height: 600
- enable "Shutdown source when not visible"
- enable "Refresh browser when scene becomes active"
- custom CSS: default is fine. Optionally you can add ".animated { animation-delay:500ms; }" in order to delay the fade-in animation. This can create a nice effect when each pilot is faded in sequencially.
