export const transpose = (data) => {
    const arr = structuredClone(data)
    for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < i; j++) {
            const tmp = arr[i][j];
            arr[i][j] = arr[j][i];
            arr[j][i] = tmp;
        }
    }
    return arr
}