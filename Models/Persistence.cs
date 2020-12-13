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
                public List<string> readIndex(string attribute) {
            List<string> serie = new List<string>();

            StreamWriter fout = new StreamWriter(attribute+".csv", false);

            serie.Add(attribute);
            fout.WriteLine(attribute);
            using (var command = _context.Database.GetDbConnection().CreateCommand())
            {
                command.CommandText = $"SELECT {attribute} FROM indici";
                _context.Database.OpenConnection();
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        fout.WriteLine(reader[attribute]);
                        serie.Add(reader[attribute].ToString());
                    }
                }
            }
            fout.Close();
            
            return serie;
        }
        
    }
}





    