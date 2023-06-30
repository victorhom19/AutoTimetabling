import {gql} from "@apollo/client";

export const GET_ITEMS = () => {
    return gql`
        query GetItems {
            items {
                name
                user {
                    id
                }
            }
        }
    `
}

export const GET_USER_PROJECTS = () => {
    return gql`
        query {
            projects {
                id
                name
                description
            }
        }
    `
}

export const GET_EDUCATION_PROGRAMS = () => {
    return gql`
        query {
            educationPrograms {
                id
                code
                name
                profileCode
                profileName
                educationLevel
            }
        }
    `
}