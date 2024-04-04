'use client';
import React, { useState } from 'react';
import axios from 'axios'; // Import Axios
import {
    Paper,
    Grid,
    Stack,
    TextField,
    FormControl,
    Button,
    RadioGroup,
    Radio,
    FormControlLabel,
    FormLabel,
} from '@mui/material';
import BaseCard from '@/app/(DashboardLayout)/components/shared/BaseCard';
import { styled } from '@mui/material/styles';

const Item = styled(Paper)(({ theme }) => ({
    ...theme.typography.body1,
    textAlign: 'center',
    color: theme.palette.text.secondary,
    height: 60,
    lineHeight: '60px',
}));

const Forms = () => {
    const [formData, setFormData] = useState({
        StudentName: '',
        TelegramID: '',
        ParentName: '',
        ParentContact: '',
        DateTime: '2024-04-08T15:00:00+08:00',
        LessonDuration: '',
        NumLessons: ""
    });

    
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        
        // Define the API endpoint
        const API_ENDPOINT = 'http://localhost:5001/onboarding/onboard_student';
    
        try {
            // Structure the payload as expected by your Flask endpoint
            const payload = {
                "name": formData.StudentName,
                "telegram": formData.TelegramID,
                "poc": [formData.ParentName, formData.ParentContact], // Adjust according to your backend expectations
                "schedule": [formData.DateTime, formData.LessonDuration, formData.NumLessons], // You'll need to fill in the Num of Lessons
            };
    
            // Make a POST request to your Flask backend with the form data
            const response = await axios.post(API_ENDPOINT, payload);
            
            console.log('Response from Flask:', response.data);
    
            // Reset the form or handle the response as needed
            setFormData({
                StudentName: '',
                TelegramID: '',
                ParentName: '',
                ParentContact: '',
                DateTime: '2024-04-08T15:00:00+08:00',
                LessonDuration: '',
                NumLessons: ""
             
            });
        } catch (error) {
            console.error('Error submitting form data:', error);
        }
    };
    

    const handleChange = (event: { target: { name: any; value: any; }; }) => {
        const { name, value } = event.target;
        setFormData({ ...formData, [name]: value });
    };

    return (
        <Grid container spacing={3}>
            <Grid item xs={12} lg={12}>
                <BaseCard title="Student Information">
                    <>
                        <form onSubmit={handleSubmit}>
                            <Stack spacing={3}>
                                <TextField
                                    id="name-basic"
                                    name="StudentName"
                                    label="Student Name"
                                    variant="outlined"
                                    value={formData.StudentName}
                                    onChange={handleChange}
                                />
                                <TextField
                                    id="telegram-basic"
                                    name="TelegramID"
                                    label="Telegram ID"
                                    variant="outlined"
                                    value={formData.TelegramID}
                                    onChange={handleChange}
                                />
                                <TextField
                                    id="Pname-basic"
                                    name="ParentName"
                                    label="Parent Name"
                                    variant="outlined"
                                    value={formData.ParentName}
                                    onChange={handleChange}
                                />
                                <TextField
                                    id="Pcontact-basic"
                                    name="ParentContact"
                                    label="Parent Telegram"
                                    variant="outlined"
                                    value={formData.ParentContact}
                                    onChange={handleChange}
                                />
                                <TextField
                                    id="DateTime-basic"
                                    name="DateTime"
                                    label="DateTime for First Lesson"
                                    variant="outlined"
                                    value={formData.DateTime}
                                    onChange={handleChange}
                                    helperText="Enter Date & Time In This Format: YYYY-MM-DDTHH:MM:SS+/-HH:MM"
                                />
                                <TextField
                                    id="Duration-basic"
                                    name="LessonDuration"
                                    label="Lesson Duration"
                                    variant="outlined"
                                    value={formData.LessonDuration}
                                    onChange={handleChange}
                                    helperText="Please Enter Duration In Hours"
                                />
                                <TextField
                                    id="NumLessons-basic"
                                    name="NumLessons"
                                    label="Number of Lessons"
                                    variant="outlined"
                                    value={formData.NumLessons}
                                    onChange={handleChange}
                                    helperText="Please Enter Number of Lessons"
                                />

                            </Stack>
                            <br />
                            <Button variant="outlined" color="primary" type="submit">
                                Submit
                            </Button>
                        </form>
                    </>
                </BaseCard>
            </Grid>
        </Grid>
    );
};

export default Forms;
