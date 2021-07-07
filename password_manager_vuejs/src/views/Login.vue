<template>
  <div class="login" >
    <v-container fluid fill-height>
    <v-alert type="error" :value="alert" dense>
      {{loginError}}
    </v-alert>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <h1> User Login</h1>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="10" md="8" lg="6" >
        <v-card ref="form" elevation="6">
          <v-card-text>
            <v-text-field ref="email" v-model="email"
              :rules="[() => !!email || 'This field is required']"
              label="Email"  required
            ></v-text-field>
            <v-text-field
              ref="password" v-model="password"
              :rules="[() => !!password || 'This field is required']"
              label="Password" required
            ></v-text-field>
          </v-card-text>
          <v-divider class="mt-12"></v-divider>
          <v-card-actions>
            <v-btn text>
              Cancel
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="submit"
            >
              Submit
            </v-btn>
          </v-card-actions>
        </v-card>
        <v-spacer></v-spacer>
        <h5>Don't You Have an Account? <router-link to="/register">Register Here</router-link></h5>
      </v-col>
    </v-row>
  </v-container>
  </div>
</template>

<script>
  export default {
    data: () => ({
      email:null,
      password:null,
      formHasErrors: false,
      loginError:null,
      alert:false,
    }),
    mounted(){
      if(alert){
        this.hide_alert();
      }
    },
    methods:{
      async userLogin(url, msg) {
        return await this.axios({
          url: url,
          method: 'POST',
          // responseType: 'application/json',
          data: msg,
        }).then((res)=>{
          console.log(res);
          var user_id = res.data.user_id
          if (res.data.response == "success"){
            this.$router.push({ name: 'Home', 
              params: { 
                data: {
                  userId: user_id,
                }
              }
            })
          }else{
            this.loginError = res.data.error;
            this.alert = true;
            
          }
        })
      },
      async submit(){
        // const validateForm = this.$refs.form.validate();
        const msg = {
          email:this.email,
          password:this.password
        }
        // console.log(validateForm);
        console.log(msg);
        // if(validateForm){
          await this.userLogin("http://localhost:5000/user/login", msg)
        // }

      },
      hide_alert() {
        window.setInterval(() => {
          this.alert = false;

        }, 5000) 
      }
    }
  }

</script>