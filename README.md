"# SFWRTECH4SA3-final" 

** INSTRUCTIONS **
    MAKE SURE YOU HAVE THE ENV VARIABLES SET UP IN YOUR .env FILE BEFORE RUNNING THE PROGRAM.

    1. ON FIRST RUN or TO RESEED: 
      Select option 3 from the main menu to set/reset the venue groups to the initial data.
    
    2. Run the program and select option 1 to view venue group reports.

    3. Select option 2 to manage venue groups, and select option 1 to add a venue, and specify the sport type.
      When adding a venue, make sure to copy & paste the name and address exactly as they appear on Google Maps for best results.
      You can try any of these sample venues or add your own:
          name | address
          * these will work and create a complete VenueDataObject with coordinates from the API:
          "Waterworks Park", "1 Waterworks Park, St Thomas, ON N5P 3S4"
          "Storybook Gardens", "1958 Storybook Ln, London, ON N6H 2N7"
          "Springbank Park", "1085 Commissioners Rd W, London, ON N6K 4Y6"

          * these will trigger the manual entry flow since they are not recognized by the API, but you can still add them by entering coordinates manually:
              If you choose to add a venue manually, you will need to enter the latitude and longitude coordinates. 
              You can find these by searching for the venue on Google Maps, right-clicking on the location, and selecting coordinates. 
          "Pickleball Courts at Burwell Park" | "465 Burwell Rd, St Thomas, ON N5P 4N6" -> 42.806126911890686, -81.15805678742016
          "1Password Park" | "355 Burwell Rd, St Thomas, ON N5P 4M3" -> 42.80172687079454, -81.16732821708126
          "Doug Tarry Complex" | "275 Bill Martyn Pkwy, St Thomas, ON N5R 1X6" -> 42.7518412560948, -81.16890730461743
    5. After adding a venue, select option 1 to view the updated reports and see how the new venue ranks against the others in its group.

    6. You can also remove venues from groups by selecting option 2 and then option 2 again, and following the prompts.

Design patterns in my project:
    Adapter
    Factory
    Null Object

Technical Architecture

    Programming Language
    Python
    Cloud Database
    Redis: Using Redis (including GEOADD) to store the user’s favourite venue coordinate groups, sports, & preferences, and cache weather/crowd data for 30 minutes to save on API calls.
    Third-Party Services
    BestTimes.app: For hourly forecasted crowd data.
    OpenWeather API: For real-time weather data, especially wind, rain, and temperature.

