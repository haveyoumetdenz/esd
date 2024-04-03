// 'use client';
// import {
//   Paper, Grid,
//   Select,
//   Button,
//   Box,
//   Stack,
//   IconButton,
//   Fab,
//   ButtonGroup,
// } from '@mui/material';
// import PageContainer from '@/app/(DashboardLayout)/components/container/PageContainer';
// import BaseCard from '@/app/(DashboardLayout)/components/shared/BaseCard';
// import { createTheme, ThemeProvider, styled } from '@mui/material/styles';
// import { IconHome, IconTrash, IconUser } from '@tabler/icons-react';


// const Item = styled(Paper)(({ theme }) => ({
//   ...theme.typography.body1,
//   textAlign: 'center',
//   color: theme.palette.text.secondary,
//   height: 60,
//   lineHeight: '60px',
// }));

// const darkTheme = createTheme({ palette: { mode: 'dark' } });
// const lightTheme = createTheme({ palette: { mode: 'light' } });

// const Buttons = () => {
//   return (
//     <PageContainer title="button" description="this is button">
//       <Grid container spacing={3}>
//         <Grid item xs={12} lg={6}>
//           <BaseCard title="Color Buttons">
//             <Stack spacing={2} direction="row">
//               <Button variant="contained" color="primary">
//                 Contained
//               </Button>
//               <Button variant="contained" color="error">
//                 Contained
//               </Button>
//               <Button variant="contained" color="secondary">
//                 Contained
//               </Button>
//               <Button variant="contained" color="success">
//                 Contained
//               </Button>
//               <Button variant="contained" color="warning">
//                 Contained
//               </Button>
//             </Stack>
//           </BaseCard>
//         </Grid>
//         <Grid item xs={12} lg={6} >
//           <BaseCard title="Text Buttons">
//             <Stack spacing={2} direction="row">
//               <Button variant="text" color="primary">Text</Button>
//               <Button variant="text" color="error">Text</Button>
//               <Button variant="text" color="secondary">Text</Button>
//               <Button variant="text" color="success">Text</Button>
//               <Button variant="text" color="warning">Text</Button>
//             </Stack>
//           </BaseCard>
//         </Grid>
//         <Grid item xs={12} lg={6} >
//           <BaseCard title="Outline Buttons">
//             <Stack spacing={2} direction="row">
//               <Button variant="outlined" color="primary">
//                 outlined
//               </Button>
//               <Button variant="outlined" color="error">
//                 outlined
//               </Button>
//               <Button variant="outlined" color="secondary">
//                 outlined
//               </Button>
//               <Button variant="outlined" color="success">
//                 outlined
//               </Button>
//               <Button variant="outlined" color="warning">
//                 outlined
//               </Button>
//             </Stack>
//           </BaseCard>
//         </Grid>
//         <Grid item xs={12} lg={6} >
//           <BaseCard title="Size Buttons">
//             <Box sx={{ "& button": { mx: 1 } }}>
//               <Button color="primary" size="small" variant="contained">
//                 small
//               </Button>
//               <Button color="error" size="medium" variant="contained">
//                 medium
//               </Button>
//               <Button color="secondary" size="large" variant="contained">
//                 large
//               </Button>
//             </Box>
//           </BaseCard>
//         </Grid>
//         <Grid item xs={12} lg={6} >
//           <BaseCard title="Icon Buttons">
//             <Stack spacing={2} direction="row">
//               <IconButton aria-label="delete" color="success">
//                 <IconHome />
//               </IconButton>
//               <IconButton aria-label="delete" color="error">
//                 <IconTrash />
//               </IconButton>
//               <IconButton aria-label="user" color="warning">
//                 <IconUser />
//               </IconButton>
//             </Stack>
//           </BaseCard>
//         </Grid>
//         <Grid item xs={12} lg={6}>
//           <BaseCard title="Fab Buttons">
//             <Stack spacing={2} direction="row">
//               <Fab color="primary" aria-label="add">
//                 <IconHome />
//               </Fab>
//               <Fab color="secondary" aria-label="add">
//                 <IconTrash />
//               </Fab>
//               <Fab color="secondary" disabled aria-label="add">
//                 <IconUser />
//               </Fab>
//             </Stack>
//           </BaseCard>
//         </Grid>
//         <Grid item xs={12} lg={6}>
//           <BaseCard title="Group Buttons">
//             <ButtonGroup
//               variant="contained"
//               aria-label="outlined primary button group"
//             >
//               <Button>One</Button>
//               <Button>Two</Button>
//               <Button>Three</Button>
//             </ButtonGroup>
//           </BaseCard>
//         </Grid>
//         <Grid item xs={12} lg={6}>
//           <BaseCard title="Group Outline Buttons">
//             <ButtonGroup variant="outlined" aria-label="outlined button group">
//               <Button>One</Button>
//               <Button>Two</Button>
//               <Button>Three</Button>
//             </ButtonGroup>
//           </BaseCard>
//         </Grid>
//       </Grid>

//     </PageContainer>
//   );
// };

// export default Buttons;

'use client';
import React, { useState } from 'react';
import { Container, TextField, MenuItem, Box, Typography, Button } from '@mui/material';
import { db } from './firebase'; // Adjust the path to your firebase.js file
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
      const communicationsRef = collection(db, 'communications');

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
