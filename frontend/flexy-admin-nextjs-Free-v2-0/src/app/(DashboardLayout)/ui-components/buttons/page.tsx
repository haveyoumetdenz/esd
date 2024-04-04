'use client';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, TextField, MenuItem, Box, Typography, Button, Paper } from '@mui/material';

interface Event {
  id: string;
  summary: string;
  start: string;
  telegram: string; // Now including Telegram username in the Event interface
}

const TutorDashboard = () => {
  const [selectedEventId, setSelectedEventId] = useState('');
  const [message, setMessage] = useState('');
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchEvents = async () => {
      setLoading(true);
      try {
        const response = await axios.get('http://localhost:5005/progress');
        setEvents(response.data); // Make sure the response data matches the Event interface
      } catch (error) {
        console.error('Failed to fetch events:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const handleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedEventId(event.target.value as string);
  };

  const sendMessageToFirebase = async () => {
    // Find the selected event based on the selectedEventId
    const selectedEvent = events.find(event => event.id === selectedEventId);
    if (!selectedEvent) {
      console.error('Selected event not found.');
      return;
    }
    
    // Using the Telegram username from the selected event
    const telegramUsername = selectedEvent.telegram;
    
    const payload = {
      telegramUsername, // Using the extracted Telegram username
      eventID: selectedEventId,
      report: message,
    };

    try {
      await axios.post('http://localhost:5005/progress/update_student_progress', payload);
      alert('Progress report sent successfully.');
    } catch (error) {
      console.error('Error sending progress report:', error);
      alert('Failed to send progress report.');
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Tutor Dashboard
          </Typography>
          {/* <Button
            variant="contained"
            color="secondary"
            
            disabled={loading}
          >
            {loading ? 'Fetching Events...' : 'Fetch Recent Events'}
          </Button> */}
          <TextField
            select
            label="Select Event"
            value={selectedEventId}
            onChange={handleChange}
            fullWidth
            margin="normal"
          >
            {events.map((event) => {
              const eventStartDate = new Date(event.start);
              const formattedStart = eventStartDate.toLocaleString('en-SG', {
                timeZone: 'Asia/Singapore',
                day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit', hour12: true
              });

              return (
                <MenuItem key={event.id} value={event.id}>
                  {`${event.summary} @ ${formattedStart} - @${event.telegram}`}
                </MenuItem>
              );
            })}
          </TextField>
          <TextField
            label="Message to Parents"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
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
            Send Progress Report
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default TutorDashboard;
