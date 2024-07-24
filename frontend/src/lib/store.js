import {writable} from 'svelte/store'


const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0)
export const keyword = persist_storage("keyword", "")
export const limit = persist_storage("limit", 10)
export const error = persist_storage("error", {'detail':[]})
