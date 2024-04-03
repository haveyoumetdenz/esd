// firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDGNuI9RnCdimLGRFzbeswqsjBT2cgSFU8",
  authDomain: "educatum-communication.firebaseapp.com",
  projectId: "educatum-communication",
  storageBucket: "educatum-communication.appspot.com",
  messagingSenderId: "309373230397",
  appId: "1:309373230397:web:711fa7a3d28a82c7157954",
  measurementId: "G-7VHSYR33DY"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db };
