<script setup lang="ts">

import NavBar from "@/components/navbar/NavBar.vue";
import {onMounted} from "vue";
import api from "@/js/http/api.ts";
import { useUserrStore } from "./stores/user";
import {useRoute, useRouter} from "vue-router";

const user = useUserrStore()
const route = useRoute()
const router = useRouter()

onMounted(async () => {
  try{
    const res =await api.get('/api/user/account/get_user_info/')
    const data = res.data
    if(data.result==='success'){
      user.setUserInfo( data)
    }
  }catch (err){

  }finally {
    user.setHasPulledUserInfo(true)

    if(route.meta.needLogin && !user.isLogin()){
      await router.replace({
        name: 'user-account-login-index'
      })
    }
  }
})
</script>

<template>
<NavBar>
  <RouterView />
</NavBar>
</template>

<style scoped>

</style>
