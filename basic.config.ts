// basic.config.ts lets you define the schema for your database
// after updating this file, you may need to restart the dev server
// docs: https://docs.basic.tech/info/schema 

export const schema = {
  project_id: '5e100a79-94b2-4117-972a-42971b63c226',
  version: 0,
  tables: {
    table_name: {
      type: 'collection',
      fields: {
        field_name: {
          type: 'string',
          indexed: true,
        }
      }
    }
  }
}
