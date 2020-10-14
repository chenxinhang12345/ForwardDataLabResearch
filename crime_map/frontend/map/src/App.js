// import React, {useState, useRef} from 'react';
// import GoogleMapReact from "google-map-react";
// import useSupercluster from "use-supercluster";
// import useSwr from "swr";
// import axios from "axios";
// import './App.css';

// export default function App(){
//   //map setup
//   const fetcher = (...args) => fetch(...args).then(response => response.json());
//   const Marker = ({children}) => children;
//   const mapRef = useRef();
//   const [zoom, setZoom] = useState(10);
//   const [bounds, setBounds] = useState(null);
//   const data_url = 'http://127.0.0.1:5000/crimeLocs';
//   const {data,error} = useSwr(data_url, fetcher)
//   // const crimes = data && !error ? data.slice(0,200) : [];
//   const crimes = [{key:1,lat:10, lng:10},{key:2,lat:20, lng:20}]
//   return (<div style = {{hieght:"100vh", width:"100%"}}>
//     <GoogleMapReact bootstrapURLKeys = {{key: }}
//     defaultCenter = {{lat:41.8781, lng: 87.6298 }}
//     defaultZoom = {10}
//     >
//       {crimes.map(crime => (
//           <Marker key ={crime.key} lat = {crime.lat} lng = {crime.lng}>
//             <div>
//               <img src = "/crime_point.svg" alt="crime"></img>
//             </div>
//           </Marker>
//       )
//       )}
//     </GoogleMapReact>
//   </div>);
// }
import React, { useState, useRef } from "react";
import useSwr from "swr";
import GoogleMapReact from "google-map-react";
import useSupercluster from "use-supercluster";
import "./App.css";

const fetcher = (...args) => fetch(...args).then(response => response.json());

const Marker = ({ children }) => children;

export default function App() {
  const mapRef = useRef();
  const [bounds, setBounds] = useState(null);
  const [zoom, setZoom] = useState(10);

  const url =
    "http://localhost:5000/crimeLocs";
  const { data, error } = useSwr(url, { fetcher });
  const crimes = data && !error ? data : [];
  console.log(crimes);
  var key = 0;
  const points = crimes.map(crime => ({
    type: "Feature",
    properties: { cluster: false, crimeId: key+=1, category: crime.category },
    geometry: {
      type: "Point",
      coordinates: [
        crime[1],
        crime[0]
      ]
    }
  }));

  const { clusters, supercluster } = useSupercluster({
    points,
    bounds,
    zoom,
    options: { radius: 75, maxZoom: 20 }
  });

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: process.env.REACT_APP_GOOGLE_KEY }}
        defaultCenter={{ lat: 41.881832, lng: -87.623177}}
        defaultZoom={10}
        yesIWantToUseGoogleMapApiInternals
        onGoogleApiLoaded={({ map }) => {
          mapRef.current = map;
        }}
        onChange={({ zoom, bounds }) => {
          setZoom(zoom);
          setBounds([
            bounds.nw.lng,
            bounds.se.lat,
            bounds.se.lng,
            bounds.nw.lat
          ]);
        }}
      >
        {clusters.map(cluster => {
          const [longitude, latitude] = cluster.geometry.coordinates;
          const {
            cluster: isCluster,
            point_count: pointCount
          } = cluster.properties;

          if (isCluster) {
            return (
              <Marker
                key={`cluster-${cluster.id}`}
                lat={latitude}
                lng={longitude}
              >
                <div
                  className="cluster-marker"
                  style={{
                    width: `${10 + (pointCount / points.length) * 20}px`,
                    height: `${10 + (pointCount / points.length) * 20}px`
                  }}
                  onClick={() => {
                    const expansionZoom = Math.min(
                      supercluster.getClusterExpansionZoom(cluster.id),
                      20
                    );
                    mapRef.current.setZoom(expansionZoom);
                    mapRef.current.panTo({ lat: latitude, lng: longitude });
                  }}
                >
                  {pointCount}
                </div>
              </Marker>
            );
          }

          return (
            <Marker
              key={`crime-${cluster.properties.crimeId}`}
              lat={latitude}
              lng={longitude}
            >
              <button className="crime-marker">
                <img src="/crime_point.svg" alt="crime" />
              </button>
            </Marker>
          );
        })}
      </GoogleMapReact>
    </div>
  );
}
