using MongoDB.Bson;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TRACE_API.Services
{
    public class MongoService
    {
        private readonly MongoHelper _reports;

        public MongoService()
        {
            _reports = new MongoHelper();
        }

        public BsonDocument GetScoreDetails(string _id)
        {
            var filter_id = Builders<BsonDocument>.Filter.Eq("_id", ObjectId.Parse(_id));
            var entity = _reports.Collection.Find(filter_id)
                .Project(Builders<BsonDocument>.Projection.Exclude("_id").Include("data"))
                .FirstOrDefault();

            return entity;
        }
    }
}