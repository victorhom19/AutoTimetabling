const {createSlice} = require("@reduxjs/toolkit");

const initialState = {
    id: null,
    name: null,
    description: null
}


const projectSlice = createSlice({
    name: 'project',
    initialState: initialState,
    reducers: {
        selectProject: (state, action) => {
            if (state.id === action.payload.id) {
                state.id = null
                state.name = null
                state.description = null
            } else {
                state.id = action.payload.id
                state.name = action.payload.name
                state.description = action.payload.description
            }
            return state

        }
    }
})

export const {actions, reducer} = projectSlice