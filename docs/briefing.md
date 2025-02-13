# **Immich family history app**

<p align="center">
  <img src="ss.png" />
</p>

## *A self-hosted web app to facilitate family photo archiving*

## Installing Python
1. `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. `uv python install 3.12`

## Bootstrap Project
1. `git clone https://github.com/marcrleonard/Remminich.git`
2. `cd Remminich`
3. `uv venv --python=3.12`
4. `source .venv/bin/activate`
5. `pip3 install -r requirements.txt`



## **Problem**

***TL;DR:** Immich is designed to handle modern ongoing storage and organization for digital photos, not a collective family archive of scanned analog photographs.*

I’ve taken on the task of scanning and cataloging a collection of thousands of negatives and prints from my family’s collection, spanning from the 1950s through the 2000s. Digitizing the photos is a project unto itself, but gathering information about the people, places, dates, and events in them is a large undertaking as well. I’ve been looking for a software solution that is self-hosted and allows multiple family members to view and collaboratively contribute metadata to this photo collection as it grows. Ideally this solution would be web-based and supports multiple users.

[Immich](https://immich.app/) is an amazing personal photo application that comes quite close\! But Immich isn’t actually meant for this family history case, and so it has lots of small issues that that make it ill-suited for this specialized task:

* Immich doesn’t allow for approximate dates – each date must have a day and time assigned, which isn’t ideal when identifying analog photos from the past.  
* Immich doesn’t allow for batch-modifying dates *relatively*. This is problematic when we know the order of a group of photos and their approximate dates. In Immich, selecting them all and changing the date disrupts their relative order, since they will all be set to a single identical timestamp.  
* Only the owner account of the photos can see and modify face/people data.  
* Only the owner account of the photos can see and modify geolocation data.  
* If we work around some of these limitations by sharing a single account/login with the whole family, we cannot have a reviewable log of changes and contributions with attribution.

In short, while Immich is amazing for organizing photos, especially in one’s personal collection, it is not fully equipped to allow a family to collaboratively add historical metadata to the photos.

## **Goal**

**This will be a companion webapp to Immich that specifically handles group metadata contributions in people, places, and dates.**

The admin – the sole uploader of the photo files themselves – curates the bulk of the Immich library. This user is likely literally an admin in Immich, and is responsible for uploading images and making sure that, for instance, photos in a given film roll have EXIF data that properly orders the photos.

The admin can create shared albums as usual in Immich. The admin could also share their credentials with others in the family if they trust them, and wish to allow them to explore the collection by face, geography, etc.

But these other contributors will be discouraged from directly manipulating the metadata of images. Instead, they will log into their own account in our new app\![^1]

## **Implementation**

### **Contributor Experience**

The app works a bit like a dating app, where users are presented with a stack of images (an Immich album). If they don’t have anything to add to the photo, they “swipe left” and the next stack is revealed.

If the contributor knows something about the photo(s), they “swipe right”. This brings them to a view where they can contribute their knowledge to the album\!

Contributors may add or modify the following metadata:

* **Date:** Year; season (a new concept, translated on the backend to the first month of each season); month; day; time. If the contributor does not specify any of these, we set it to a reasonable default (ie. “1” for day, “January” for year, etc.). Contributors should be strongly discouraged from editing individual photos’ dates. In most cases, they should add/change dates at the album level, which adjusts all photos in that album relative to the first photo. (This should be made clear in the UI somehow.)  
* **Comments:** Encourage contributors to add context and stories at the album and image level  
* **Location:** Allow contributors to search for locations from the OpenStreetView data that Immich uses.[^2]

Crucially, this can work on the album or image level. If the user is given a group of photos – an album – they can either apply this metadata to all images in the album, or drill down into a single image to change it alone.

Once contributors make changes or additions, they are written back to the Immich database. These changes are also written to the app’s console log, and/or the album’s metadata, and/or the app’s page for this album.

### **Needy photos algorithm**

The app will maintain its own “neediness scores” for albums. Within each album, the app will keep track of how many enclosed photos have date, comment, and location data set. An album’s neediness is defined as:

*(\[Total number of images with dates set later than the “modern” threshold[^3]\] \+ \[Total number of images with no comments\] \+ \[Total number of images with no location\]) / (\[Total number of images in album \* 3\] \* 100\)*

The higher the score, the more needy the album is – and the more important it is that contributors add information. **At any moment, the album with the highest neediness is shown to the next contributor.** The idea is that over time, the software prioritizes putting needy images in front of users, gradually filling in the historical info in a way that’s organic, collaborative, and efficient.

## **Open questions**

* What to do about photos that don’t neatly belong in albums, like unsorted scans of prints? Should these be added to a special album that contains one-off photos? Should each photo in that group carry its own neediness score?  
* How does authorization and security work here? The way Immich works today, only the owner of a photo is allowed to modify its non-comment metadata. Should our app use the admin’s API key and allow users to act as if they are the admin? 😬  
* Future enhancement: allow contributors to define sub-albums, or split albums up? This would cover the case where a single roll of film, represented in Immich as an album, actually encompasses multiple events, times, places, etc.  
* This spec doesn’t account for faces/people at all. How might we integrate that sort of labeling into this app? Do we need to at all, if contributors have access to the main Immich app on the admin account? This may be solved for us by [revised Partner Sharing permissioning coming to Immich](https://github.com/immich-app/immich/discussions/7038) soon.

[^1]: For simplicity’s sake, this could also be a more simple “What’s your name?” text field. The goal here is to write attributable log entries when metadata is modified, so that the admin can track down contributors, if need be.

[^2]: Easier said than done, I imagine. MVP could be either an open text field or raw lat/long coordinates.

[^3]: Images in Immich need to have a date of *some sort*. In order to classify some images as needing a date, we must set a “modern threshold” – a date after which we consider the image to need a manually set date (This could be hardcoded into the app or configurable by the admin). In most cases, it will be safe to set this date around the time the digitization began. The important thing is that this date is *after* the newest photo in the collection was taken.


# To run
`fastapi dev main.py`