import {gql} from "@apollo/client";

export const CREATE_PROJECT = (projectName, projectDescription) => {
    return gql`
        mutation {
            createProject(name: "${projectName}", description: "${projectDescription}") {
                id
                name
                description
            }
        }
    `
}

export const CREATE_EDUCATION_PROGRAM = (code, name, profileCode, profileName, educationLevel) => {
    return gql`
        mutation {
            createEducationProgram(code: "${code}", name: "${name}", profileCode: "${profileCode}",
             profileName: "${profileName}", educationLevel: "${educationLevel}") {
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

export const DELETE_EDUCATION_PROGRAM =
    gql`
        mutation DeleteEducationProgram($itemId: Int!) {
            deleteEducationProgram(id: $itemId) {
                id
            }
        }
    `