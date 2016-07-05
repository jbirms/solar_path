# solar_path

The advent of solar energy production presents a unique challenge in predicting how much energy you will be generating. This value depends on many factors: latitude, longitude, time of day, time of year, elevation, and cloud cover. This challenge is amplified when you're dealing with solar powered cars, where the location is always changing, and short-term timescales matter much more because your car's ability to move fully depends on how much sun you are getting.

This app creates a google maps polyline, breaks it into fixed length intervals, calculates estimated solar energy at each point, and interpolates/integrates between them to total up the solar energy along a path.


