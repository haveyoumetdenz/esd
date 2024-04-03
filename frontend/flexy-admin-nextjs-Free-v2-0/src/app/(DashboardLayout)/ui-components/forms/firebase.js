

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyC8Nbl_exM-iRKBE7UFlGMT9lVJfqcdHgk",
    authDomain: "educatum-onboarding.firebaseapp.com",
    projectId: "educatum-onboarding",
    storageBucket: "educatum-onboarding.appspot.com",
    messagingSenderId: "578746782121",
    appId: "1:578746782121:web:6edc18d483ed0c744b74b8",
    measurementId: "G-LKCYR3HJ38"
  };
  
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app)
  const db = getFirestore(app); // Get Firestore database instance
  
  export { app, auth, db };