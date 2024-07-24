<script>
    import fastapi from "../lib/api"
    import {push} from 'svelte-spa-router'
    import moment from 'moment/min/moment-with-locales'
    import Error from '../components/Error.svelte'
    import {marked} from 'marked'

    moment.locale('ko')

    export let params = {}
    let photo_id = params.photo_id

    let photo = {description: ""}
    let previewImage = {image: ""}
    let headers = {}
    let change_decs = false
    let change_name = false

    let error = {detail: []}

    async function get_photo() {
        await fastapi("get", "/api/photo/detail/" + photo_id, {}, (json) => {
            photo = json.photo
            previewImage = json.image
            headers = JSON.parse(photo.headers)
            console.log(photo, previewImage, headers)
        })
    }

    let promise = null;
    let desc = photo.description
    let name = photo.name

    async function post_description(event) {
        event.preventDefault()
        let url = "/api/photo/description/" + photo_id
        let params = {
            content: desc
        }
        await fastapi('post', url, params,
            (json) => {
                change_decs = false
                desc = ''
                error = {detail: []}
                get_photo()
            },
            (err_json) => {
                error = err_json
            }
        )
    }

    async function download_file() {
        await window.open(import.meta.env.VITE_SERVER_URL + '/api/photo/download/' + photo_id)
        let downloader = document.getElementById('downloader')
        downloader.className = "btn btn-success btn-lg"
        downloader.value = 'Download Complete!'
    }

    $: promise = get_photo();
    $: console.log(1);

    async function edit_name(event) {
        event.preventDefault()
        console.log(event.keyCode)
        if (event.keyCode === 13) {
            name = document.getElementById('filename').innerText
            let url = "/api/photo/rename/" + photo_id
            let params = {
                content: name
            }
            await fastapi('post', url, params,
                (json) => {
                    change_name = false
                    error = {detail: []}
                    get_photo()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
</script>

{#await promise}
    <p>...waiting</p>
{:then message}
    <div class="container my-3">
        <!-- 질문 -->
        <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex justify-content-start">
                <h2 id="filename" class="border-bottom py-2 me-3" contenteditable={change_name.toString()} on:keypress={(e) => edit_name(e)} style="-ms-ime-mode: auto">{photo.name}</h2>
                <div class="d-flex align-items-center">
                    <input type="button" value="Rename" class="btn {change_name && 'btn-dark'} {!change_name && 'btn-outline-dark'}" on:click={() => change_name = !change_name}/>
                </div>
            </div>
            <div>
                <input id="downloader" type="button" value="Download .FITS file" class="btn btn-outline-info btn-lg" on:click={download_file}/>
            </div>
        </div>
        <div class="card my-3">
            <div class="card-body">
                <div class="row">
                    <div class="col-6 d-flex justify-content-center">
                        <div class="d-flex align-items-baseline">
                            <div class="sticky-top">
                                <figure class="figure mt-5">
                                    <img src="data:image/jpg;base64,{previewImage}" alt="사진 로딩 실패. 새로 고침 해 주세요." class="img-fluid rounded"/>
                                </figure>
                            </div>
                        </div>
                    </div>
                    <div class="col-6 d-flex justify-content-center">
                        <div class="table-responsive col-12">
                            <table class="table rounded h-auto align-middle">
                                <thead>
                                <tr class="table-dark">
                                    <th class="col-4 text-center">Keyword</th>
                                    <th class="col-4 text-center">Value</th>
                                    <th class="col-4 text-center">Comment</th>
                                </tr>
                                </thead>
                                <tbody>
                                {#each Object.keys(headers) as header}
                                    <tr class="h-auto">
                                        <td class="col-4 text-center">
                                            <div class="h-auto">{header}</div>
                                        </td>
                                        <td class="col-4 text-center">
                                            <div class="h-auto">{headers[header][0]}</div>
                                        </td>
                                        <td class="col-4 text-center">
                                            <div class="h-auto">{headers[header][1]}</div>
                                        </td>
                                    </tr>
                                {/each}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="d-flex justify-content-end">
                    <div class="badge bg-light text-dark p-2">
                        {moment(photo.create_date).format("YYYY년 MM월 DD일 a hh:mm")}
                    </div>
                </div>
            </div>
        </div>
        <button class="btn btn-secondary" on:click="{() => {push('/')}}">목록으로</button>
        <!-- 답변 목록 -->
        <div class="card my-3">
            <div class="card-body">
                {#if photo.description === ""}
                    <div class="card-text text-black-50" style="white-space: pre-line;">no description (MarkDown이 적용되어 있습니다.)</div>
                {:else}
                    <div class="card-text">{@html marked.parse(photo.description)}</div>
                {/if}
            </div>
        </div>
        <!-- 답변 등록 -->
        <div class="d-flex justify-content-between">
            <input type="submit" value="update description" class="btn btn-primary" on:click="{() => change_decs = !change_decs}">
            {#if change_decs}
                <input type="submit" value="update" class="btn btn-success" on:click="{post_description}"/>
            {/if}
        </div>
        {#if change_decs}
            <Error error={error}/>
            <form method="post" class="my-3">
                <div class="mb-3">
                    <textarea rows="10" bind:value={desc} class="form-control"/>
                </div>
            </form>
        {/if}
    </div>
{/await}