# Eskom load shedding schedule viewer

Simple Single-Page App (SPA) to view the Eskom load shedding schedule for a given zone and stage, for a range of supported South African cities. Schedules have been manually transformed into JSON files, which support varying blocks and schedule types (days of the week or days of the month).

The website is built using Vue, Buefy and Bulma, with Yarn as the package manager and Parcel as the bundler. and is hosted on Netlify.

There is also a series of Python scripts, running on an Azure VM, that scrape supported city websites to extract the current load shedding stage (where available).

## Run local

The following command starts a local dev server on http://localhost:1234, with Parcel building, serving and watching.

```bash
yarn dev
```

## Build

Release builds are built using the following command, and are deployed into the `dist/` subdirectory.

```bash
yarn build
``` 

