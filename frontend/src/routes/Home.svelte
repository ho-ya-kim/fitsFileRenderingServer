<script>
    import fastapi from "../lib/api"
    import {link, push} from 'svelte-spa-router'
    import {page, keyword, limit} from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    import {Fileupload} from 'flowbite-svelte';

    moment.locale('ko')

    let photo_list = []
    let total = 0
    let kw = ''
    let lm = ''
    $: total_page = Math.ceil(total / $limit)


    async function get_photo_list() {
        let params = {
            page: $page,
            keyword: $keyword,
            size: $limit,
        }
        await fastapi('get', '/api/photo/list', params, (json) => {
            photo_list = json.photo_list
            total = json.total
            kw = $keyword
            lm = $limit
        })
    }

    const search = function () {
        $keyword = kw
        $page = 0
        $limit = lm
        get_photo_list($page)
        // push('/photo/' + photo_id)
    }

    let files;

    $: if (files) {
        console.log(files)
    }

    async function upload_file(event) {
        event.preventDefault()

        for (let i = 0; i < files.length; i += 1) {
            const data = files[i]
            console.log(data)
            if (data === 0) {
                continue
            }
            let url = "/api/photo/upload"
            let formData = new FormData()
            formData.append('file', data)
            await fetch(import.meta.env.VITE_SERVER_URL + url, {
                    method: 'post',
                    body: formData
                }
            ).then(res => {
                get_photo_list()
                res.json().then(json => {
                    console.log(json)
                    get_photo_list($page)
                })
            })
            let uploader = document.getElementById('uploadButton')
            uploader.className = "btn btn-success float-end"
            uploader.innerText = 'Upload Complete!'
            await get_photo_list($page)
        }
    }

    let promise = null;
    $: $page;
    $: $keyword;
    $: promise = get_photo_list($page);
    $: $limit;
</script>

<meta name="viewport" content="width=1280">
{#await promise}
    <p>...waiting</p>
{:then message}
    <div class="container my-3">
        <div class="row my-3">
            <div class="col-12 my-1">
                <div class="input-group">
                    <input class="btn btn-outline-secondary disabled" value="검색 키워드" style="color: black">
                    <input type="text" class="form-control btn-outline-info" bind:value="{kw}" placeholder="검색 키워드를 입력하세요">
                    <input class="btn btn-outline-secondary disabled" value="한 페이지당 항목 수" style="color: black">
                    <input type="number" min="1" max="100" class="form-control btn-outline-info" bind:value="{lm}" placeholder="자연수를 입력하세요. (1 ~ 100)">
                    <button class="btn btn-outline-secondary" on:click={search}>
                        찾기
                    </button>
                </div>
            </div>
            <div class="col my-1">
                <div class="btn-toolbar d-flex justify-content-between" role="toolbar">
                    <div class="input-group-prepend me-1" role="group">
                        <Fileupload placeholder="파일을 선택해 주세요. 여러 파일을 선택할 수 있습니다." bind:files id="uploader" multiple class="form-control btn-outline-info" content-type="multipart/form-data" accept=".fits"/>
                    </div>
                    <div class="btn-group ms-1" role="group">
                        <button type="button" class="btn btn-outline-info" id="uploadButton" on:click="{upload_file}">Upload .FITS file</button>
                    </div>
                </div>
            </div>
        </div>
        {#if total === 0}
            <h1 class="pagination justify-content-center">검색 결과가 없습니다.</h1>
        {:else}
            <table class="table">
                <thead>
                <tr class="table-dark">
                    <th>번호</th>
                    <th>이름</th>
                    <th>업로드 시간</th>
                </tr>
                </thead>
                <tbody>
                {#each photo_list as photo, i}
                    <tr>
                        <td>{ i + ($page * $limit) + 1}</td>
                        <td>
                            <a use:link href="/detail/{photo.id}">{photo.name}</a>
                        </td>
                        <td>{moment(photo.create_date).format("YYYY년 MM월 DD일 a hh:mm")}</td>
                    </tr>
                {/each}
                </tbody>
            </table>
            <!-- 페이징처리 시작 -->
            <ul class="pagination justify-content-center">
                {#if 5 < $page}
                    <li class="page-item">
                        <button class="page-link" on:click="{() => $page = 0}">처음</button>
                    </li>
                {/if}
                <!-- 이전페이지 -->
                <li class="page-item {$page <= 0 && 'disabled'}">
                    <button class="page-link" on:click="{() => $page--}">이전</button>
                </li>
                <!-- 페이지번호 -->
                {#each Array(total_page) as _, loop_page}
                    {#if loop_page >= $page - 5 && loop_page <= $page + 5}
                        <li class="page-item {loop_page === $page && 'active'}">
                            <button on:click="{() => $page = loop_page}" class="page-link">{loop_page + 1}</button>
                        </li>
                    {/if}
                {/each}
                <!-- 다음페이지 -->
                <li class="page-item {$page >= total_page-1 && 'disabled'}">
                    <button class="page-link" on:click="{() => $page++}">다음</button>
                </li>
                {#if $page < total_page - 6}
                    <li class="page-item">
                        <button class="page-link" on:click="{() => $page = total_page - 1}">끝</button>
                    </li>
                {/if}
            </ul>
        {/if}
        <!-- 페이징처리 끝 -->
    </div>
{/await}
