<script>
    import Router from 'svelte-spa-router'
    import Home from "./routes/Home.svelte"
    import Detail from "./routes/Detail.svelte"
    import Navigation from "./components/Navigation.svelte"

    const routes = {
        '/': Home,
        '/detail/:photo_id': Detail,
    }
</script>

<Navigation />
<Router {routes}/>
