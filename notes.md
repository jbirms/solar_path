### Notes for solar_path

from [Predicting Solar Generation from Weather Forecasts Using Machine Learning](http://www.ecs.umass.edu/~irwin/smartgridcomm.pdf)

Tips on weather -> solar correlation:
  * sky cover, RH% and precipitation are highly correlated with eachother and solar intensity
  * temp, dew point, wind speed are partially correlated with eachother and solar intensity
    * my guess is that these parameters would affect sky cover and its variability
  * support vector machines (SVM) with radial basis function fernels built using historical data is the most accurate approach
  * they use 5-min interval data from a weather station at UMass Amherst and compare prediction to reality. 
    * [here](http://traces.cs.umass.edu/index.php/Sensors/Sensors) is that data set.
    * this data confirmed that solar intensity strongly depends on cloud cover: some summer days had **less** total energy intensity than winter days!


#### UI design
  * origin, destination, and date-time of departure on the top of the page
  * map of the route is the main section of the page, right below the fields above
    * not sure if we should use leaflet or google maps for the actual map display...
    * map's path line color will vary based on energy intensity (like a heatmap but just a line).
  * below the map will be a value vs time plot of solar energy vs time


