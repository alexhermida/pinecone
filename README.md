[![Build Status](https://travis-ci.org/alexhermida/pinecone.svg?branch=master)](https://travis-ci.org/alexhermida/pinecone)

# Vigotech.org

## Pinecone managament site

Application for basic management of events inside medium size communities and groups. Its purpose is to help
groups organizers to have a picture of future and past events within the community.

* Allow events creation
* Integration with google calendar
* Integration with Twitter (WIP)
* Integration with Telegram Bot (WIP)


## Backend

* Django w/ DRF
* PostreSQL

Environment variables needed:

    `GOOGLE_APPLICATION_CREDENTIALS`
    `GOOGLE_CALENDAR_ID`

## Frontend

* VueJS with Vuetify