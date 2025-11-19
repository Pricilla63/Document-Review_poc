// // import { defineConfig } from 'vite'
// // import react from '@vitejs/plugin-react'

// // // https://vite.dev/config/
// // export default defineConfig({
// //   plugins: [react()],
// // })


// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'

// export default defineConfig({
//   plugins: [react()],
//   resolve: {
//     alias: {
//       'react-is': require.resolve('react-is')
//     }
//   },
//   optimizeDeps: {
//     include: ['react-is']
//   }
// })



import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      'react-is': fileURLToPath(new URL('./node_modules/react-is', import.meta.url))
    }
  },
  optimizeDeps: {
    include: ['react-is']
  }
})