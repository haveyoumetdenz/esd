'use client'
import { Grid, Box } from '@mui/material';
import PageContainer from '@/app/(DashboardLayout)/components/container/PageContainer';
// components
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import googleCalendarPlugin from '@fullcalendar/google-calendar';
import { useState } from 'react';

export default function Home() {
  const [events, setEvents] = useState([
    {
      googleCalendarId: '434c3a6f1d477740be91e0f73d98da3dfbcbef70d299c5a53c542d3e40e29de5@group.calendar.google.com',
      className: 'event'
    }
  ]);
  console.log(events)
  return (
    <>
      <nav className="flex justify-between mb-12 border-b border-violet-100 p-4 ">
        <h1 className="font-bold text-2xl text-gray-700">Calendar</h1>  
      </nav>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <div className="grid grid-cols-10">
          <div>
            <FullCalendar
              plugins={[dayGridPlugin, timeGridPlugin, googleCalendarPlugin]}
              headerToolbar={{
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek'
              }}
              initialView="dayGridMonth"
              nowIndicator={true}
              selectMirror={true}
              googleCalendarApiKey='AIzaSyCRTHDapEDol-cgIeerOAcaq_QptuM9F18'
              eventSources={events}
            />
          </div>
        </div>
      </main>
    </>
  );
}
