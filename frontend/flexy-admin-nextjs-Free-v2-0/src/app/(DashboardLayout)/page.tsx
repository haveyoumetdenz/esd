'use client'
import { Grid, Box } from '@mui/material';
import PageContainer from '@/app/(DashboardLayout)/components/container/PageContainer';
// components
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin, { Draggable, DropArg} from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';
import googleCalendarPlugin from '@fullcalendar/google-calendar';
import { use, useState } from 'react';

let INITIAL_EVENTS = [
  {
      googleCalendarId:'https://calendar.google.com/calendar/ical/denzel.toh.2022%40smu.edu.sg/public/basic.ics',
      className:'event'
  }
]

export default function Home() {
  return (
  <>
  <iframe src="https://calendar.google.com/calendar/embed?src=denzel.toh.2022%40smu.edu.sg&ctz=Asia%2FSingapore" allowFullScreen width="100%" height="500px"></iframe>
  {/* <nav className="flex justify-between mb-12 border-b border-violet-100 p-4 ">
    <h1 className="font-bold text-2x1 text-gray-700">Calendar</h1>  
  </nav>
  <main className="flex min-h-screen flex-col items-center justify-between p-24">
    <div className="grid grid-cols-10">
      <div>
      <FullCalendar
        plugins={[
          dayGridPlugin,
          interactionPlugin,
          timeGridPlugin,
          googleCalendarPlugin
        ]}
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth, timeGridWeek'
        }}
        initialView="dayGridWeek"
        nowIndicator={true}
        selectMirror={true}
        googleCalendarApiKey='AIzaSyDtfQJvVR3xySXrLTVXgSnOCVFOprFcKyM'
        eventSources={{googleCalendarId: "https://calendar.google.com/calendar/embed?src=denzel.toh.2022%40smu.edu.sg&ctz=Asia%2FSingapore"}}
      />
      </div>
    </div>
    </main> */}
  </>
)}
