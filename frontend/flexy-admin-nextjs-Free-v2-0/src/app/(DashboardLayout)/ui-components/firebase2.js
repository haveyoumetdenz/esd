import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig2 = {
  apiKey: "AIzaSyDGNuI9RnCdimLGRFzbeswqsjBT2cgSFU8",
  authDomain: "educatum-communication.firebaseapp.com",
  projectId: "educatum-communication",
  storageBucket: "educatum-communication.appspot.com",
  messagingSenderId: "309373230397",
  appId: "1:309373230397:web:711fa7a3d28a82c7157954",
  measurementId: "G-7VHSYR33DY"
};

const app2 = initializeApp(firebaseConfig2, "firebase2");
const auth2 = getAuth(app2);
const db2 = getFirestore(app2);

export { app2 as app, auth2 as auth, db2 as db };