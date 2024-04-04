'use client';
import React, { useState } from 'react';
import { Container, TextField, MenuItem, Box, Typography, Button, Paper } from '@mui/material';
import { db as db2 } from '../firebase2'; // Adjust the path to your firebase.js file
import { collection, addDoc } from 'firebase/firestore';

const TutorDashboard = () => {
  const [selectedModule, setSelectedModule] = useState('');
  const [message, setMessage] = useState('');

  // Dummy data for completed coding modules
  const completedModules = [
    { id: 'mod01', title: 'JavaScript - Basics', studentId: 'ID001' },
    { id: 'mod02', title: 'Python - Data Structures', studentId: 'ID002' },
    { id: 'mod03', title: 'Java - Object-Oriented Programming', studentId: 'ID003' },
  ];

  const handleChange = (event: { target: { value: any; }; }) => {
    const moduleId = event.target.value;
    setSelectedModule(moduleId);

    // Find the selected module based on the moduleId
    const xxx = completedModules.find(module => module.id === moduleId);
    if (xxx) {
      // Generate a detailed template message based on the selected module
      setMessage(`Student ID: ${xxx.studentId}\nModule: ${xxx.title}\nToday, we covered the topic "${xxx.title}" in class. The student showed excellent understanding of the concepts and was able to apply them effectively in coding exercises.`);
    }
  };

  const sendMessageToFirebase = async () => {
    try {
      // Create a reference to the communications collection
      const communicationsRef = collection(db2, 'communications');

      // Add a new document to the communications collection
      const newCommunicationRef = await addDoc(communicationsRef, {
        studentID: selectedModule.split('-')[0].trim(), // Extracting student ID from the selected module
        CompletedModule: selectedModule.split('-')[1].trim(), // Extracting module title from the selected module
        MessageToParents: message,
        dateSent: new Date().toISOString().split('T')[0] // Format the date as "YYYY-MM-DD"
      });

      console.log('New communication added with ID:', newCommunicationRef.id);
    } catch (error) {
      console.error('Error adding communication to Firebase:', error);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Tutor Dashboard
          </Typography>
          <TextField
            select
            label="Select Completed Module"
            value={selectedModule}
            onChange={handleChange}
            fullWidth
            margin="normal"
          >
            {completedModules.map((module) => (
              <MenuItem key={module.id} value={module.id}>
                {`Student ID: ${module.studentId} - ${module.title}`}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Message to Parents"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            multiline
            rows={15}
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
        </Paper>
      </Box>
    </Container>
  );
};

export default TutorDashboard;
