
'use client';
import React, { useState } from 'react';
import { Container, TextField, MenuItem, Box, Typography, Button } from '@mui/material';
import { db as db2 } from '../firebase2'; // Adjust the path to your firebase.js file
import { collection, addDoc } from 'firebase/firestore';

const TutorDashboard = () => {
  const [selectedLesson, setSelectedLesson] = useState('');
  const [message, setMessage] = useState('');
  const [selectedStudentId, setSelectedStudentId] = useState('');

  // Dummy data for completed lessons
  const completedLessons = [
    { id: 1, title: 'Math - Algebra' },
    { id: 2, title: 'Science - Biology' },
    { id: 3, title: 'History - World War II' },
  ];

  const handleChange = (event) => {
    const lessonId = event.target.value;
    setSelectedLesson(lessonId);

    // Find the selected lesson based on the lessonId
    const lesson = completedLessons.find(lesson => lesson.id === parseInt(lessonId));
    if (lesson) {
      // Generate a template message based on the selected lesson
      setMessage(`Today, we covered the topic "${lesson.title}" in class. The student showed good understanding and progress.`);
    }
  };

  const sendMessageToFirebase = async () => {
    try {
      // Create a reference to the communications collection
      const communicationsRef = collection(db2, 'communications');

      // Add a new document to the communications collection
      const newCommunicationRef = await addDoc(communicationsRef, {
        studentID: selectedStudentId,
        CompletedLessons: selectedLesson,
        MessageToParents: message,
        dateSent: new Date().toISOString().split('T')[0] // Format the date as "YYYY-MM-DD"
      });

      console.log('New communication added with ID:', newCommunicationRef.id);
    } catch (error) {
      console.error('Error adding communication to Firebase:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ my: 4 }}>
        <Typography variant="h5" gutterBottom>
          Tutor Dashboard
        </Typography>
        <TextField
          label="Student ID"
          value={selectedStudentId}
          onChange={(event) => setSelectedStudentId(event.target.value)}
          fullWidth
          margin="normal"
        />
        <TextField
          select
          label="Completed Lessons"
          value={selectedLesson}
          onChange={handleChange}
          fullWidth
          margin="normal"
        >
          {completedLessons.map((lesson) => (
            <MenuItem key={lesson.id} value={lesson.id}>
              {lesson.title}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          label="Message to Parents"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          multiline
          rows={4}
          fullWidth
          margin="normal"
        />
        <Button
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
          onClick={sendMessageToFirebase}
        >
          Send Message
        </Button>
      </Box>
    </Container>
  );
};

export default TutorDashboard;
