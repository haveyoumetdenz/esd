'use client';
import React, { useState } from 'react';
import { db as db1} from '../firebase1'; // Import the db instance from the file you created
import { collection, doc, getDocs ,setDoc} from 'firebase/firestore'; // Import Firestore collection, addDoc, and getDocs functions

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
        Gender: 'female',
    });

    
    const handleSubmit = async (event: { preventDefault: () => void; }) => {
        event.preventDefault();
    
        try {
            // Get the current count of documents in the collection
            const querySnapshot = await getDocs(collection(db1, 'Students'));
            const documentCount = querySnapshot.size;
    
            // Generate the document ID with padded zeros
            const documentId = String(documentCount + 1).padStart(3, '0');
    
            // Set the document with the specified ID
            await setDoc(doc(db1, 'Students', documentId), formData);
    
            console.log('Form data submitted successfully');
            console.log('Document written with ID: ', documentId);
    
            // Optionally, reset form fields after submission
            setFormData({
                StudentName: 'Nirav Joshi',
                TelegramID: '',
                ParentName: '',
                ParentContact: '',
                DateTime: '2024-04-08T15:00:00+08:00',
                LessonDuration: '',
                Gender: 'female',
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
                                    label="Parent Contact"
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
                                    helperText="Please enter the date and time in the format: YYYY-MM-DDTHH:MM:SS+/-HH:MM"
                                />
                                <TextField
                                    id="Duration-basic"
                                    name="LessonDuration"
                                    label="Lesson Duration"
                                    variant="outlined"
                                    value={formData.LessonDuration}
                                    onChange={handleChange}
                                    helperText="Please enter duration in Hours"
                                />

                                <FormControl>
                                    <FormLabel id="demo-radio-buttons-group-label">Gender</FormLabel>
                                    <RadioGroup
                                        aria-labelledby="demo-radio-buttons-group-label"
                                        defaultValue="female"
                                        name="Gender"
                                        value={formData.Gender}
                                        onChange={handleChange}
                                    >
                                        <FormControlLabel
                                            value="female"
                                            control={<Radio />}
                                            label="Female"
                                        />
                                        <FormControlLabel
                                            value="male"
                                            control={<Radio />}
                                            label="Male"
                                        />
                                        <FormControlLabel
                                            value="other"
                                            control={<Radio />}
                                            label="Other"
                                        />
                                    </RadioGroup>
                                </FormControl>
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
