def build_itinerary_prompt(destination, start_date, end_date, travel_style, dietary_prefs, budget):
    return f"""
You are an expert travel planner. Create a detailed day-by-day itinerary for the following trip.

Trip details:
- Destination: {destination}
- Start date: {start_date}
- End date: {end_date}
- Travel style: {travel_style}
- Dietary preferences: {dietary_prefs}
- Budget level: {budget}

Format the itinerary exactly like this:

## Day 1 — [Date] — [Theme for the day]

**Morning**
- Where to eat breakfast with a specific restaurant recommendation
- Activity with specific neighborhood or landmark name

**Afternoon**
- Where to eat lunch with a specific restaurant recommendation
- Activity with practical details (cost, how to get there)

**Evening**
- Where to eat dinner with a specific restaurant recommendation
- Activity or area to explore

**Logistics tip:** One practical tip for the day (transport, booking ahead, best time to arrive somewhere)

---

Repeat for every day of the trip. Be specific — use real neighborhood names, real restaurant names, and real attractions. Avoid generic advice like "visit the city center" or "try local food."
Prioritize restaurants, landmarks and activities that local people recommend over touristy attractions. Refer to Reddit posts to find the best spots.
For each restaurant, activity or landmark, include a hyperlink to the google maps search page of the landmark or restaurant, and embed it right on the location or restaurant name. 
The Google Maps search link should be in this exact format: https://www.google.com/maps/search/PLACE+NAME+CITY with spaces replaced by + signs.
For each activity, landmark or restaurant, at the beginning of your bullet, include the recommended start time and end time. Account for transportation time when you plan.
"""