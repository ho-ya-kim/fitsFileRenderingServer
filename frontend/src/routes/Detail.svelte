<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import {push} from 'svelte-spa-router'
    import moment from 'moment/min/moment-with-locales'
    import { marked } from 'marked'
    moment.locale('ko')

    export let params = {}
    let photo_id = params.photo_id

    let photo = {description: ""}
    let change_decs = false

    let error = {detail: []}

    async function get_photo() {
        await fastapi("get", "/api/photo/detail/" + photo_id, {}, (json) => {
            photo = json
            console.log(photo)
        })
    }

    let promise = get_photo();
    let desc = photo.description

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
</script>

{#await promise}
    <p>...waiting</p>
{:then message}
    <div class="container my-3">
        <!-- 질문 -->
        <h2 class="border-bottom py-2">{photo.name}</h2>
        <div class="card my-3">
            <div class="card-body">
                <div class="card-text" style="white-space: pre-line;">{photo.imagePath}</div>
                <div class="card-text" style="white-space: pre-line;">{photo.headers}</div>
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
            <input type="submit" value="update description" class="btn btn-primary" on:click="{() => change_decs = ~change_decs}">
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