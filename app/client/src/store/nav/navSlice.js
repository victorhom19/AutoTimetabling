const {createSlice} = require("@reduxjs/toolkit");


export const NavModes = {
    HOME: 'HOME',

    PROJECT_CREATE_TAB: 'PROJECT_CREATE_TAB',
    PROJECT_SELECT_TAB: 'PROJECT_SELECT_TAB',

    DATABASE_EDUCATION_PROGRAM_TAB: 'DATABASE_EDUCATION_PROGRAM_TAB',
    DATABASE_CLASSROOM_TAB: 'DATABASE_CLASSROOMS_TAB',
    DATABASE_INSTITUTION_TAB: 'DATABASE_INSTITUTION_TAB',

    TIMETABLE_TIMESLOTS_TAB: 'TIMETABLE_TIMESLOTS',
    TIMETABLE_CLASSROOM_AVAILABILITY_TAB: 'TIMETABLE_CLASSROOM_AVAILABILITY',
    TIMETABLE_PREFERENCES_TAB: 'TIMETABLE_TIMESLOTS',
    TIMETABLE_COURSES_TAB: 'TIMETABLE_TIMESLOTS',
    TIMETABLE_CREATE_TAB: 'TIMETABLE_TIMESLOTS',

}

const navSlice = createSlice({
    name: 'nav',
    initialState: NavModes.HOME,
    reducers: {
        setNavMode: (state, action) => {
            state = action.payload
            return state
        }
    }
})

export const {actions, reducer} = navSlice
