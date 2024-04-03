import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig1 = {
  apiKey: "AIzaSyC8Nbl_exM-iRKBE7UFlGMT9lVJfqcdHgk",
  authDomain: "educatum-onboarding.firebaseapp.com",
  projectId: "educatum-onboarding",
  storageBucket: "educatum-onboarding.appspot.com",
  messagingSenderId: "578746782121",
  appId: "1:578746782121:web:6edc18d483ed0c744b74b8",
  measurementId: "G-LKCYR3HJ38"
};

const app1 = initializeApp(firebaseConfig1, "firebase1");
const auth1 = getAuth(app1);
const db1 = getFirestore(app1);

export { app1 as app, auth1 as auth, db1 as db };
