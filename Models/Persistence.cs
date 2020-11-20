using System;
using Microsoft.Data.Sqlite;
using System.Collections.Generic;
using SsdWebApi.Models;
using Microsoft.EntityFrameworkCore;
using System.IO;

namespace SsdWebApi {
    public class Persistence {
    
        private  readonly  IndiceContext _context;
        public Persistence ( IndiceContext context ) {

            _context = context;
           
        }
            public List<string> readIndex(int id){

                List<string> serie =new List<string>();   
                string[] indices = new string []{"id","Data","FTSE_MIB","GOLD_SPOT","MSCI_EM","MSCI_EURO","All_Bonds","US_TReasury"};
                string attribute =indices[id];

                //StreamWriter fout =new StreamWriter(attribute+".csv",false);

                serie.Add(attribute);
               // fout.WriteLine(attribute);

                using(var command  =_context.Database.GetDbConnection().CreateCommand())
                {
                    command.CommandText =$"SELECT {attribute} From indici ";
                    _context.Database.OpenConnection();

                    using (var reader = command.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                          //  fout.WriteLine(reader[attribute]);
                            serie.Add(reader[attribute].ToString() );
                        }
                    }

                }
                //fout.Close();

                return serie;

            }
        // public void testDB () {
        //     var connectionStringBuilder = new SqliteConnectionStringBuilder ();
        //     //Use DB in project directory. If it does not exist, create it:
        //     connectionStringBuilder.DataSource = "./finindices.sqlite";
        //     using (var connection = new SqliteConnection (connectionStringBuilder.ConnectionString)) {
        //         connection.Open ();

        //     }
        // }

    }
}




    